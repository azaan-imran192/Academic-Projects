from django.urls import path
from . import views

urlpatterns = [
    path("images/", views.list_images),
    path("images/<int:image_id>/traits/", views.image_traits),

    # ✅ NEW (non-conflicting)
    path("traits/temporal/", views.plant_temporal),

    path("images/<int:image_id>/leaves/", views.image_leaf_segments), 

    path("filters/", views.image_filters),
]