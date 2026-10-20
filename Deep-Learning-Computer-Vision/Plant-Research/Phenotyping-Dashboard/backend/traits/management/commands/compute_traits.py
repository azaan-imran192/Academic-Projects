# from pathlib import Path

# from django.conf import settings
# from django.core.management.base import BaseCommand

# from traits.models import PlantImage, PlantTraits
# from traits.pipeline.segmenter import run_segmentation_for_image
# from traits.engine_b.traits_from_segmented import (
#     compute_traits_from_segmented_dir,
#     compute_plant_traits_from_raw_image,
# )

# class Command(BaseCommand):
#     help = "Compute Path-B traits (DINO + FastSAM) for PlantImage and store in PlantTraits"

#     def add_arguments(self, parser):
#         parser.add_argument("--limit", type=int, default=None)
#         parser.add_argument("--plant_id", type=int, default=None)

#     def handle(self, *args, **options):
#         qs = PlantImage.objects.all().order_by("id")

#         if options["plant_id"] is not None:
#             qs = qs.filter(plant_id=options["plant_id"])

#         if options["limit"] is not None:
#             qs = qs[: options["limit"]]

#         media_root = Path(settings.MEDIA_ROOT)

#         done = 0

#         for img in qs:
#             abs_path = media_root / img.rel_path

#             if not abs_path.exists():
#                 self.stdout.write(
#                     self.style.WARNING(
#                         f"Missing file: {abs_path} (image id={img.id})"
#                     )
#                 )
#                 continue

#             try:
#                 plant_traits = compute_plant_traits_from_raw_image(abs_path)
#                 seg_info = run_segmentation_for_image(abs_path, media_root)

#                 segmented_dir = Path(seg_info["segmented_dir"])
#                 leaf_traits = compute_traits_from_segmented_dir(segmented_dir)

#                 merged = {
#                     "plant": plant_traits,
#                     "leaf": leaf_traits,
#                 }

#                 PlantTraits.objects.update_or_create(
#                     image=img,
#                     defaults={"traits": merged},
#                 )

#                 done += 1

#             except Exception as e:
#                 self.stdout.write(
#                     self.style.WARNING(
#                         f"Failed image id={img.id}: {e}"
#                     )
#                 )
#                 continue

#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"Computed + saved traits for {done} images."
#             )
#         )

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from traits.models import PlantImage, PlantTraits, PlantTraitsMySQL
from traits.pipeline.segmenter import run_segmentation_for_image
from traits.engine_b.traits_from_segmented import (
    compute_traits_from_segmented_dir,
    compute_plant_traits_from_raw_image,
)


def push_to_mysql(img, plant_traits, leaf_traits):
    """Push flattened traits to remote MySQL (pheno_lums.plant_traits)."""
    try:
        PlantTraitsMySQL.objects.update_or_create(
            image_id=img.id,
            defaults={
                "plant_id":     img.plant_id,
                "date_folder":  img.date_folder,
                "camera":       img.camera,
                "filename":     img.filename,

                "plant_leaf_area_px":         plant_traits.get("leaf_area_px", 0),
                "plant_aspect_ratio":         plant_traits.get("aspect_ratio", 0),
                "plant_solidity":             plant_traits.get("solidity", 0),
                "plant_vigor_pct":            plant_traits.get("vigor_pct", 0),
                "plant_color_uniformity_pct": plant_traits.get("average_color_uniformity_pct", 0),
                "plant_chlorophyll_level":    plant_traits.get("chlorophyll_level", 0),
                "plant_texture_entropy":      plant_traits.get("texture_entropy", 0),
                "plant_chlorosis_pct":        plant_traits.get("chlorosis_pct", 0),
                "plant_health_score":         plant_traits.get("health_score", 0),

                "leaf_count":                 leaf_traits.get("leaf_count", 0),
                "leaf_area_px":               leaf_traits.get("leaf_area_px", 0),
                "leaf_aspect_ratio":          leaf_traits.get("aspect_ratio", 0),
                "leaf_solidity":              leaf_traits.get("solidity", 0),
                "leaf_vigor_pct":             leaf_traits.get("vigor_pct", 0),
                "leaf_color_uniformity_pct":  leaf_traits.get("average_color_uniformity_pct", 0),
                "leaf_chlorophyll_level":     leaf_traits.get("chlorophyll_level", 0),
                "leaf_texture_entropy":       leaf_traits.get("texture_entropy", 0),
                "leaf_chlorosis_pct":         leaf_traits.get("chlorosis_pct", 0),
                "leaf_health_score":          leaf_traits.get("health_score", 0),
            },
        )
        return True
    except Exception as e:
        return False, str(e)


class Command(BaseCommand):
    help = "Compute traits (DINO + FastSAM) and save to SQLite + MySQL"

    def add_arguments(self, parser):
        parser.add_argument("--limit",    type=int, default=None)
        parser.add_argument("--plant_id", type=int, default=None)
        parser.add_argument(
            "--skip-mysql",
            action="store_true",
            default=False,
            help="Only save to SQLite, skip MySQL push",
        )

    def handle(self, *args, **options):
        qs = PlantImage.objects.all().order_by("id")

        if options["plant_id"] is not None:
            qs = qs.filter(plant_id=options["plant_id"])

        if options["limit"] is not None:
            qs = qs[: options["limit"]]

        media_root = Path(settings.MEDIA_ROOT)
        skip_mysql = options["skip_mysql"]

        done = 0
        failed = 0
        mysql_failed = 0

        for img in qs:
            abs_path = media_root / img.rel_path

            if not abs_path.exists():
                self.stdout.write(
                    self.style.WARNING(f"Missing file: {abs_path} (image id={img.id})")
                )
                failed += 1
                continue

            try:
                # Step 1: Plant-level traits from raw image
                plant_traits = compute_plant_traits_from_raw_image(abs_path)

                # Step 2: Segment leaves + compute leaf-level traits
                seg_info = run_segmentation_for_image(abs_path, media_root)
                segmented_dir = Path(seg_info["segmented_dir"])
                leaf_traits = compute_traits_from_segmented_dir(segmented_dir)

                merged = {"plant": plant_traits, "leaf": leaf_traits}

                # Step 3a: Save to local SQLite
                PlantTraits.objects.update_or_create(
                    image=img,
                    defaults={"traits": merged},
                )

                # Step 3b: Save to remote MySQL
                if not skip_mysql:
                    result = push_to_mysql(img, plant_traits, leaf_traits)
                    if result is True:
                        mysql_status = "SQLite + MySQL ✓"
                    else:
                        mysql_status = f"SQLite only (MySQL failed: {result[1]})"
                        mysql_failed += 1
                else:
                    mysql_status = "SQLite only (--skip-mysql)"

                self.stdout.write(self.style.SUCCESS(
                    f"  id={img.id} | {leaf_traits.get('leaf_count', 0)} leaves"
                    f" | {mysql_status}"
                ))
                done += 1

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"  Failed image id={img.id}: {e}")
                )
                failed += 1
                continue

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. Computed: {done} | Failed: {failed}"
            + (f" | MySQL failures: {mysql_failed}" if mysql_failed else "")
        ))