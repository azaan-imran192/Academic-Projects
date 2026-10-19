"""
Management command: create_mysql_table

Creates the plant_traits table on the remote MySQL server (pheno_lums).
Run this ONCE before pushing any data.

Usage:
    python manage.py create_mysql_table

Place at: traits/management/commands/create_mysql_table.py
"""

from django.core.management.base import BaseCommand
from django.db import connections


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS plant_traits (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,

    -- Link to local PlantImage
    image_id        INT NOT NULL,
    plant_id        INT DEFAULT NULL,
    date_folder     VARCHAR(20)  NOT NULL,
    camera          VARCHAR(10)  NOT NULL,
    filename        VARCHAR(255) NOT NULL,

    -- Plant-level traits (from raw image HSV mask)
    plant_leaf_area_px              DOUBLE DEFAULT 0,
    plant_aspect_ratio              DOUBLE DEFAULT 0,
    plant_solidity                  DOUBLE DEFAULT 0,
    plant_vigor_pct                 DOUBLE DEFAULT 0,
    plant_color_uniformity_pct      DOUBLE DEFAULT 0,
    plant_chlorophyll_level         DOUBLE DEFAULT 0,
    plant_texture_entropy           DOUBLE DEFAULT 0,
    plant_chlorosis_pct             DOUBLE DEFAULT 0,
    plant_health_score              DOUBLE DEFAULT 0,

    -- Leaf-level traits (averaged from segmented leaves)
    leaf_count                      INT    DEFAULT 0,
    leaf_area_px                    DOUBLE DEFAULT 0,
    leaf_aspect_ratio               DOUBLE DEFAULT 0,
    leaf_solidity                   DOUBLE DEFAULT 0,
    leaf_vigor_pct                  DOUBLE DEFAULT 0,
    leaf_color_uniformity_pct       DOUBLE DEFAULT 0,
    leaf_chlorophyll_level          DOUBLE DEFAULT 0,
    leaf_texture_entropy            DOUBLE DEFAULT 0,
    leaf_chlorosis_pct              DOUBLE DEFAULT 0,
    leaf_health_score               DOUBLE DEFAULT 0,

    -- Metadata
    computed_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_image (image_id),
    INDEX idx_plant_date (plant_id, date_folder),
    INDEX idx_camera (camera),
    INDEX idx_date_folder (date_folder)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


class Command(BaseCommand):
    help = "Creates the plant_traits table on the remote MySQL server (pheno_lums)"

    def handle(self, *args, **options):
        self.stdout.write("Connecting to MySQL (mysql_wwf)...")

        try:
            conn = connections["mysql_wwf"]
            conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS("Connected OK."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection failed: {e}"))
            self.stdout.write("Make sure SSH tunnel is open:")
            self.stdout.write("  ssh -L 3307:172.18.0.2:3306 root@172.104.187.5 -N")
            return

        try:
            with conn.cursor() as cursor:
                cursor.execute(CREATE_TABLE_SQL)
            self.stdout.write(self.style.SUCCESS(
                "plant_traits table created successfully on pheno_lums!"
            ))

            # Verify
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'plant_traits'")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS(
                        "Verified: plant_traits table exists in pheno_lums."
                    ))
                    # Show columns
                    cursor.execute("DESCRIBE plant_traits")
                    cols = cursor.fetchall()
                    self.stdout.write(f"\nTable has {len(cols)} columns:")
                    for col in cols:
                        self.stdout.write(f"  {col[0]} ({col[1]})")
                else:
                    self.stdout.write(self.style.WARNING(
                        "Table creation may have failed — not found in SHOW TABLES."
                    ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create table: {e}"))