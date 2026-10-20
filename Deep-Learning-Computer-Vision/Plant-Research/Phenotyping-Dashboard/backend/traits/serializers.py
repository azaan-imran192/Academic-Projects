from rest_framework import serializers
from .models import PlantImage, PlantTraits


class PlantImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    has_traits = serializers.SerializerMethodField()

    class Meta:
        model = PlantImage
        fields = "__all__"  # includes rel_path etc.
        # we will add fields dynamically by overriding:
        # DRF doesn't auto include SerializerMethodField in __all__
        # so we must list explicitly:
        fields = [
            "id", "plant_id", "date_folder", "camera", "filename", "rel_path", "created_at",
            "image_url", "has_traits",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        return request.build_absolute_uri("/media/" + obj.rel_path)

    def get_has_traits(self, obj):
        return hasattr(obj, "traits")


class PlantTraitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantTraits
        fields = "__all__"