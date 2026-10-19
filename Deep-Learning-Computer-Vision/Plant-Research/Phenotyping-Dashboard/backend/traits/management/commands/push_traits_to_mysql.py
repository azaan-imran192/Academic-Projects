"""
Management command: push_traits_to_mysql

One-time backfill: reads all 364 PlantTraits records from local SQLite
and pushes them into the plant_traits table on pheno_lums (MySQL).

Usage:
    python manage.py push_traits_to_mysql
    python manage.py push_traits_to_mysql --batch 50   # custom batch size

Place at: traits/management/commands/push_traits_to_mysql.py
"""

from django.core.management.base import BaseCommand
from django.db import connections

from traits.models import PlantTraits


INSERT_SQL = """
INSERT INTO plant_traits (
    image_id, plant_id, date_folder, camera, filename,

    plant_leaf_area_px, plant_aspect_ratio, plant_solidity,
    plant_vigor_pct, plant_color_uniformity_pct, plant_chlorophyll_level,
    plant_texture_entropy, plant_chlorosis_pct, plant_health_score,

    leaf_count, leaf_area_px, leaf_aspect_ratio, leaf_solidity,
    leaf_vigor_pct, leaf_color_uniformity_pct, leaf_chlorophyll_level,
    leaf_texture_entropy, leaf_chlorosis_pct, leaf_health_score
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON DUPLICATE KEY UPDATE
    plant_id                  = VALUES(plant_id),
    date_folder               = VALUES(date_folder),
    camera                    = VALUES(camera),
    filename                  = VALUES(filename),

    plant_leaf_area_px        = VALUES(plant_leaf_area_px),
    plant_aspect_ratio        = VALUES(plant_aspect_ratio),
    plant_solidity            = VALUES(plant_solidity),
    plant_vigor_pct           = VALUES(plant_vigor_pct),
    plant_color_uniformity_pct= VALUES(plant_color_uniformity_pct),
    plant_chlorophyll_level   = VALUES(plant_chlorophyll_level),
    plant_texture_entropy     = VALUES(plant_texture_entropy),
    plant_chlorosis_pct       = VALUES(plant_chlorosis_pct),
    plant_health_score        = VALUES(plant_health_score),

    leaf_count                = VALUES(leaf_count),
    leaf_area_px              = VALUES(leaf_area_px),
    leaf_aspect_ratio         = VALUES(leaf_aspect_ratio),
    leaf_solidity             = VALUES(leaf_solidity),
    leaf_vigor_pct            = VALUES(leaf_vigor_pct),
    leaf_color_uniformity_pct = VALUES(leaf_color_uniformity_pct),
    leaf_chlorophyll_level    = VALUES(leaf_chlorophyll_level),
    leaf_texture_entropy      = VALUES(leaf_texture_entropy),
    leaf_chlorosis_pct        = VALUES(leaf_chlorosis_pct),
    leaf_health_score         = VALUES(leaf_health_score),

    computed_at               = CURRENT_TIMESTAMP;
"""


def _g(d, key, default=0.0):
    """Safely get a float value from a dict."""
    try:
        v = d.get(key, default)
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _gi(d, key, default=0):
    """Safely get an int value from a dict."""
    try:
        v = d.get(key, default)
        return int(v) if v is not None else default
    except (TypeError, ValueError):
        return default


class Command(BaseCommand):
    help = "Backfill all 364 SQLite PlantTraits records into MySQL pheno_lums.plant_traits"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch",
            type=int,
            default=25,
            help="Number of records to insert per batch (default: 25)",
        )

    def handle(self, *args, **options):
        batch_size = options["batch"]

        # Check MySQL connection
        self.stdout.write("Checking MySQL connection...")
        try:
            conn = connections["mysql_wwf"]
            conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS("MySQL connected OK."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"MySQL connection failed: {e}"))
            self.stdout.write("Make sure SSH tunnel is open:")
            self.stdout.write("  ssh -L 3307:172.18.0.2:3306 root@172.104.187.5 -N")
            return

        # Check table exists
        try:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'plant_traits'")
                if not cursor.fetchone():
                    self.stdout.write(self.style.ERROR(
                        "plant_traits table not found! Run first:\n"
                        "  python manage.py create_mysql_table"
                    ))
                    return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Table check failed: {e}"))
            return

        # Load all SQLite records
        total = PlantTraits.objects.count()
        self.stdout.write(f"\nFound {total} trait records in SQLite.")
        self.stdout.write(f"Pushing to MySQL in batches of {batch_size}...\n")

        qs = PlantTraits.objects.select_related("image").all().order_by("id")

        done = 0
        failed = 0
        batch = []

        for pt in qs:
            img = pt.image
            t = pt.traits or {}
            plant = t.get("plant", {})
            leaf = t.get("leaf", {})

            row = (
                # identifiers
                img.id,
                img.plant_id,
                img.date_folder,
                img.camera,
                img.filename,

                # plant-level
                _g(plant, "leaf_area_px"),
                _g(plant, "aspect_ratio"),
                _g(plant, "solidity"),
                _g(plant, "vigor_pct"),
                _g(plant, "average_color_uniformity_pct"),
                _g(plant, "chlorophyll_level"),
                _g(plant, "texture_entropy"),
                _g(plant, "chlorosis_pct"),
                _g(plant, "health_score"),

                # leaf-level
                _gi(leaf, "leaf_count"),
                _g(leaf, "leaf_area_px"),
                _g(leaf, "aspect_ratio"),
                _g(leaf, "solidity"),
                _g(leaf, "vigor_pct"),
                _g(leaf, "average_color_uniformity_pct"),
                _g(leaf, "chlorophyll_level"),
                _g(leaf, "texture_entropy"),
                _g(leaf, "chlorosis_pct"),
                _g(leaf, "health_score"),
            )
            batch.append(row)

            # Flush batch
            if len(batch) >= batch_size:
                inserted, errors = self._flush(conn, batch, done)
                done += inserted
                failed += errors
                batch = []
                self.stdout.write(
                    f"  Progress: {done}/{total} pushed "
                    f"({'✓' if errors == 0 else f'{errors} errors'})"
                )

        # Flush remaining
        if batch:
            inserted, errors = self._flush(conn, batch, done)
            done += inserted
            failed += errors

        self.stdout.write("")
        if failed == 0:
            self.stdout.write(self.style.SUCCESS(
                f"Done! {done}/{total} records pushed to MySQL pheno_lums.plant_traits"
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f"Done with errors. Pushed: {done} | Failed: {failed}"
            ))

        # Final count verification
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM plant_traits")
                mysql_count = cursor.fetchone()[0]
                self.stdout.write(
                    f"\nVerification — MySQL plant_traits row count: {mysql_count}"
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not verify count: {e}"))

    def _flush(self, conn, batch, offset):
        """Insert a batch of rows. Returns (inserted_count, error_count)."""
        try:
            with conn.cursor() as cursor:
                cursor.executemany(INSERT_SQL, batch)
            conn.connection.commit()
            return len(batch), 0
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  Batch error at offset {offset}: {e}"))
            return 0, len(batch)