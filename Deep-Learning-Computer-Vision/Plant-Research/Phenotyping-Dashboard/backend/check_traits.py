from traits.models import PlantTraits

total = PlantTraits.objects.count()
print(f"Total trait records: {total}")

plant_zero_health    = 0
plant_zero_chlorosis = 0
plant_zero_vigor     = 0
plant_zero_chloro    = 0
plant_missing        = 0

leaf_zero_health     = 0
leaf_zero_chlorosis  = 0
leaf_zero_vigor      = 0
leaf_zero_count      = 0
leaf_missing         = 0

for pt in PlantTraits.objects.all():
    t = pt.traits or {}
    p = t.get("plant", {})
    l = t.get("leaf", {})

    if not p:
        plant_missing += 1
    else:
        if not p.get("health_score"):      plant_zero_health    += 1
        if not p.get("chlorosis_pct"):     plant_zero_chlorosis += 1
        if not p.get("vigor_pct"):         plant_zero_vigor     += 1
        if not p.get("chlorophyll_level"): plant_zero_chloro    += 1

    if not l:
        leaf_missing += 1
    else:
        if not l.get("health_score"):  leaf_zero_health    += 1
        if not l.get("chlorosis_pct"): leaf_zero_chlorosis += 1
        if not l.get("vigor_pct"):     leaf_zero_vigor     += 1
        if not l.get("leaf_count"):    leaf_zero_count     += 1

print(f"\n--- PLANT TRAITS (zero or missing) out of {total} ---")
print(f"  no plant dict at all: {plant_missing}")
print(f"  health_score:         {plant_zero_health}")
print(f"  chlorosis_pct:        {plant_zero_chlorosis}")
print(f"  vigor_pct:            {plant_zero_vigor}")
print(f"  chlorophyll_level:    {plant_zero_chloro}")

print(f"\n--- LEAF TRAITS (zero or missing) out of {total} ---")
print(f"  no leaf dict at all:  {leaf_missing}")
print(f"  health_score:         {leaf_zero_health}")
print(f"  chlorosis_pct:        {leaf_zero_chlorosis}")
print(f"  vigor_pct:            {leaf_zero_vigor}")
print(f"  leaf_count:           {leaf_zero_count}")