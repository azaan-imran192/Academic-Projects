from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlantDailyRecord(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="records")
    date = models.DateField()

    # Core metrics
    health_score = models.FloatField()
    color_uniformity = models.FloatField()
    chlorosis = models.FloatField()
    vigor = models.FloatField()
    leaf_count = models.IntegerField()
    leaf_area = models.FloatField()

    # Shape metrics
    aspect_ratio = models.FloatField()
    solidity = models.FloatField()

    # Optional extra metrics
    chlorophyll = models.FloatField(null=True, blank=True)
    texture_entropy = models.FloatField(null=True, blank=True)

    # For weekly stress chart
    stress = models.FloatField()

    def __str__(self):
        return f"{self.plant.name} - {self.date}"


class WeatherForecast(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="weather")
    day = models.CharField(max_length=10)  # "Mon", "Tue", etc.
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.plant.name} - {self.day}"
