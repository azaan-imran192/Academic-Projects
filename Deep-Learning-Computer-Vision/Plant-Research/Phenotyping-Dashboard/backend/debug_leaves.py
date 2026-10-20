from pathlib import Path
from django.conf import settings
from traits.models import PlantImage

media_root = Path(settings.MEDIA_ROOT)

# Check first 5 images
for img in PlantImage.objects.all().order_by("id")[:5]:
    rel_without_ext = img.rel_path.replace(".jpg", "").replace(".JPG", "")
    seg_dir = media_root / "segmented" / rel_without_ext

    print(f"\nImage id={img.id}")
    print(f"  rel_path:    {img.rel_path}")
    print(f"  looking for: {seg_dir}")
    print(f"  exists:      {seg_dir.exists()}")

    if seg_dir.exists():
        files = list(seg_dir.glob("masked_object_*.png"))
        print(f"  leaf files:  {[f.name for f in files]}")

# Also show what's actually in media/segmented/
seg_base = media_root / "segmented"
print(f"\n\nActual structure under media/segmented/:")
for p in sorted(seg_base.rglob("masked_object_*.png"))[:5]:
    print(f"  {p.relative_to(media_root)}")