from rest_framework import serializers
from .models import Plant, PlantDailyRecord, WeatherForecast


class PlantDailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantDailyRecord
        fields = "__all__"


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = "__all__"


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ["id", "name", "species", "image_url"]


class PlantDashboardSerializer(serializers.Serializer):
    plant = PlantSerializer()
    latest = PlantDailyRecordSerializer()
    health_trend = serializers.ListField()
    stress_trend = serializers.ListField()
    weather = WeatherForecastSerializer(many=True)
    recommendation = serializers.CharField()
