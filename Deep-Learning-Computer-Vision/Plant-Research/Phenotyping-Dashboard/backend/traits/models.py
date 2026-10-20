from django.db import models


class PlantImage(models.Model):
    # optional: link to a plant if you have Plant model in plants app
    plant_id = models.IntegerField(null=True, blank=True)

    date_folder = models.CharField(max_length=20)   # "2025-02-24"
    camera = models.CharField(max_length=10)        # "CAM1"
    filename = models.CharField(max_length=255)     # "CAM1_....jpg"

    # store relative path from MEDIA_ROOT
    rel_path = models.CharField(
        max_length=500
    )  # "raw_images/2025-02-24/CAM1_....jpg"

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rel_path


class PlantTraits(models.Model):
    image = models.OneToOneField(
        PlantImage,
        on_delete=models.CASCADE,
        related_name="traits"
    )

    # easiest: store all traits as JSON
    traits = models.JSONField(default=dict)

    computed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Traits for {self.image_id}"


class PlantTraitsMySQL(models.Model):
    """
    Maps to plant_traits table on remote MySQL (pheno_lums).
    managed = False means Django never creates/migrates this table.
    The db_router sends all queries for this model to 'mysql_wwf'.
    """

    # Link back to PlantImage by integer (not a real FK — cross-db)
    image_id        = models.IntegerField(unique=True)
    plant_id        = models.IntegerField(null=True, blank=True)
    date_folder     = models.CharField(max_length=20)
    camera          = models.CharField(max_length=10)
    filename        = models.CharField(max_length=255)

    # Plant-level traits (from raw image)
    plant_leaf_area_px          = models.FloatField(default=0)
    plant_aspect_ratio          = models.FloatField(default=0)
    plant_solidity              = models.FloatField(default=0)
    plant_vigor_pct             = models.FloatField(default=0)
    plant_color_uniformity_pct  = models.FloatField(default=0)
    plant_chlorophyll_level     = models.FloatField(default=0)
    plant_texture_entropy       = models.FloatField(default=0)
    plant_chlorosis_pct         = models.FloatField(default=0)
    plant_health_score          = models.FloatField(default=0)

    # Leaf-level traits (averaged across segmented leaves)
    leaf_count                  = models.IntegerField(default=0)
    leaf_area_px                = models.FloatField(default=0)
    leaf_aspect_ratio           = models.FloatField(default=0)
    leaf_solidity               = models.FloatField(default=0)
    leaf_vigor_pct              = models.FloatField(default=0)
    leaf_color_uniformity_pct   = models.FloatField(default=0)
    leaf_chlorophyll_level      = models.FloatField(default=0)
    leaf_texture_entropy        = models.FloatField(default=0)
    leaf_chlorosis_pct          = models.FloatField(default=0)
    leaf_health_score           = models.FloatField(default=0)

    computed_at = models.DateTimeField(auto_now=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False             # Django won't touch this table
        db_table = "plant_traits"   # exact MySQL table name

    def __str__(self):
        return f"MySQL Traits image_id={self.image_id}"