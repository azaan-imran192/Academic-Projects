# plants/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Plant
from .serializers import (
    PlantSerializer,
    PlantDailyRecordSerializer,
    WeatherForecastSerializer,
)


class PlantDashboardAPIView(APIView):
    def get(self, request, plant_id):
        plant = get_object_or_404(Plant, id=plant_id)

        # Most recent records first
        records = plant.records.order_by("-date")
        latest = records.first()

        # Last 7 days (reverse so oldest -> newest)
        last_records = list(records[:7])[::-1]

        health_trend = [r.health_score for r in last_records]
        stress_trend = [r.stress for r in last_records]

        weather = plant.weather.all()

        data = {
            "plant": PlantSerializer(plant).data,
            "latest": PlantDailyRecordSerializer(latest).data,
            "health_trend": health_trend,
            "stress_trend": stress_trend,
            "weather": WeatherForecastSerializer(weather, many=True).data,
            "recommendation": "Increase watering frequency slightly.",
        }

        return Response(data)


@api_view(["GET"])
def plant_temporal_dashboard(request, plant_id):
    """
    Return LAST N daily records (not necessarily calendar days).
    So ?days=7,30,90 just means 'last N entries' for this plant.
    """
    # Default to last 7 records if param missing
    try:
        days = int(request.GET.get("days", 7))
    except ValueError:
        days = 7

    plant = get_object_or_404(Plant, id=plant_id)

    # Take last N records (most recent first), then reverse to oldest→newest
    qs = plant.records.order_by("-date")[:days]
    entries = list(qs)[::-1]

    return Response(
        {
            "health": [e.health_score for e in entries],
            "chlorosis": [e.chlorosis for e in entries],
            "vigor": [e.vigor for e in entries],
            "chlorophyll": [e.chlorophyll for e in entries],
            # Optional: stress if you add a chart later
            # "stress": [e.stress for e in entries],
            "timestamps": [e.date.isoformat() for e in entries],
        }
    )
