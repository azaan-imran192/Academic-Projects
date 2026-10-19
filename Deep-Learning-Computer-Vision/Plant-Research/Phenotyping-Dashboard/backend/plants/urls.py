from django.urls import path
from . import views

urlpatterns = [
    path(
        "plant/<int:plant_id>/dashboard/",
        views.PlantDashboardAPIView.as_view(),
        name="plant-dashboard",
    ),

    path(
        "plant/<int:plant_id>/temporal/",
        views.plant_temporal_dashboard,
        name="plant-temporal",
    ),
]
