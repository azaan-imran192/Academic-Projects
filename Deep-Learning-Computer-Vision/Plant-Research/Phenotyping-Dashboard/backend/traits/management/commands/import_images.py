from django.core.management.base import BaseCommand
from traits.models import PlantImage
from pathlib import Path

class Command(BaseCommand):
    help = "Import plant images from media/raw_images into database"

    def handle(self, *args, **kwargs):
        base_dir = Path("media/raw_images")

        if not base_dir.exists():
            self.stdout.write(self.style.ERROR("media/raw_images folder not found"))
            return

        for date_dir in base_dir.iterdir():
            if not date_dir.is_dir():
                continue

            for img in date_dir.glob("*.jpg"):
                camera = img.name.split("_")[0]  # ✅ EDIT: extract CAM1/CAM2 from filename

                PlantImage.objects.update_or_create(  # ✅ EDIT: was get_or_create
                    rel_path=f"raw_images/{date_dir.name}/{img.name}",
                    defaults={
                        "plant_id": 1,               # ✅ EDIT: assign default plant
                        "date_folder": date_dir.name,
                        "camera": camera,            # ✅ EDIT: required field
                        "filename": img.name,
                    }
                )

        self.stdout.write(self.style.SUCCESS("Images imported/updated successfully"))