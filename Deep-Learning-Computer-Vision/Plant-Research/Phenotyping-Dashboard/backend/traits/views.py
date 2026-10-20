# from collections import defaultdict
# from pathlib import Path

# from django.conf import settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from .models import PlantImage, PlantTraits, PlantTraitsMySQL
# from .serializers import PlantImageSerializer, PlantTraitsSerializer


# @api_view(["GET"])
# def list_images(request):
#     plant_id = request.GET.get("plant_id")

#     qs = PlantImage.objects.all().order_by("-date_folder", "camera", "filename")
#     if plant_id:
#         qs = qs.filter(plant_id=plant_id)

#     data = PlantImageSerializer(qs, many=True).data

#     for row in data:
#         row["image_url"] = request.build_absolute_uri("/media/" + row["rel_path"])

#     return Response(data)


# @api_view(["GET"])
# def image_traits(request, image_id: int):
#     """
#     GET /api/images/<image_id>/traits/

#     Reads from MySQL first (pheno_lums.plant_traits).
#     Falls back to local SQLite if MySQL has no record for this image.
#     Response shape is identical either way — frontend needs no changes.
#     """

#     # ── Try MySQL first ──────────────────────────────────────────────────────
#     try:
#         obj = PlantTraitsMySQL.objects.get(image_id=image_id)

#         # Build the same response shape the frontend already expects
#         return Response({
#             "image": image_id,
#             "computed_at": obj.computed_at,
#             "traits": {
#                 "plant": {
#                     "leaf_area_px":                 obj.plant_leaf_area_px,
#                     "aspect_ratio":                 obj.plant_aspect_ratio,
#                     "solidity":                     obj.plant_solidity,
#                     "vigor_pct":                    obj.plant_vigor_pct,
#                     "average_color_uniformity_pct": obj.plant_color_uniformity_pct,
#                     "chlorophyll_level":            obj.plant_chlorophyll_level,
#                     "texture_entropy":              obj.plant_texture_entropy,
#                     "chlorosis_pct":                obj.plant_chlorosis_pct,
#                     "health_score":                 obj.plant_health_score,
#                 },
#                 "leaf": {
#                     "leaf_count":                   obj.leaf_count,
#                     "leaf_area_px":                 obj.leaf_area_px,
#                     "aspect_ratio":                 obj.leaf_aspect_ratio,
#                     "solidity":                     obj.leaf_solidity,
#                     "vigor_pct":                    obj.leaf_vigor_pct,
#                     "average_color_uniformity_pct": obj.leaf_color_uniformity_pct,
#                     "chlorophyll_level":            obj.leaf_chlorophyll_level,
#                     "texture_entropy":              obj.leaf_texture_entropy,
#                     "chlorosis_pct":                obj.leaf_chlorosis_pct,
#                     "health_score":                 obj.leaf_health_score,
#                 },
#             },
#         })

#     except PlantTraitsMySQL.DoesNotExist:
#         pass
#     except Exception:
#         # MySQL unreachable (tunnel closed etc.) — fall through to SQLite
#         pass

#     # ── Fallback: local SQLite ───────────────────────────────────────────────
#     try:
#         obj = PlantTraits.objects.get(image_id=image_id)
#         return Response(PlantTraitsSerializer(obj).data)
#     except PlantTraits.DoesNotExist:
#         return Response(
#             {"detail": "Traits not found"},
#             status=status.HTTP_404_NOT_FOUND,
#         )


# def _get_float_nested(d: dict, keys: list[str]):
#     cur = d
#     for k in keys:
#         if not isinstance(cur, dict) or k not in cur:
#             return None
#         cur = cur.get(k)
#     if cur is None:
#         return None
#     try:
#         return float(cur)
#     except (TypeError, ValueError):
#         return None


# @api_view(["GET"])
# def plant_temporal(request):
#     """
#     GET /api/traits/temporal/?plant_id=1&days=30&camera=CAM2

#     Reads from MySQL first, falls back to SQLite.
#     """

#     plant_id = request.GET.get("plant_id")
#     camera   = request.GET.get("camera")
#     days     = request.GET.get("days", "7")

#     if not plant_id:
#         return Response(
#             {"detail": "plant_id is required"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     try:
#         plant_id = int(plant_id)
#     except ValueError:
#         return Response(
#             {"detail": "plant_id must be an integer"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     try:
#         days = int(days)
#     except ValueError:
#         return Response(
#             {"detail": "days must be an integer"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # ── Try MySQL first ──────────────────────────────────────────────────────
#     try:
#         qs_mysql = PlantTraitsMySQL.objects.filter(plant_id=plant_id)
#         if camera:
#             qs_mysql = qs_mysql.filter(camera=camera)

#         if qs_mysql.exists():
#             return _temporal_from_mysql(qs_mysql, plant_id, camera, days)
#     except Exception:
#         # MySQL unreachable — fall through to SQLite
#         pass

#     # ── Fallback: local SQLite ───────────────────────────────────────────────
#     return _temporal_from_sqlite(plant_id, camera, days)


# def _temporal_from_mysql(qs, plant_id, camera, days):
#     """Build temporal response from MySQL PlantTraitsMySQL records."""

#     last_dates = list(
#         qs.values_list("date_folder", flat=True)
#         .distinct()
#         .order_by("-date_folder")[:days]
#     )

#     if not last_dates:
#         return _empty_temporal(plant_id, camera, days)

#     qs = qs.filter(date_folder__in=last_dates)

#     sums = defaultdict(lambda: defaultdict(float))
#     cnts = defaultdict(lambda: defaultdict(int))

#     for obj in qs:
#         d = obj.date_folder
#         for key, val in [
#             ("health",      obj.plant_health_score),
#             ("chlorosis",   obj.plant_chlorosis_pct),
#             ("vigor",       obj.plant_vigor_pct),
#             ("chlorophyll", obj.plant_chlorophyll_level),
#         ]:
#             if val is not None:
#                 sums[key][d] += val
#                 cnts[key][d] += 1

#     timestamps = sorted(last_dates)

#     def avg(key, d):
#         n = cnts[key].get(d, 0)
#         return (sums[key][d] / n) if n else None

#     return Response({
#         "plant_id":   plant_id,
#         "camera":     camera,
#         "range_days": days,
#         "timestamps": timestamps,
#         "health":      [avg("health", d)      for d in timestamps],
#         "chlorosis":   [avg("chlorosis", d)   for d in timestamps],
#         "vigor":       [avg("vigor", d)        for d in timestamps],
#         "chlorophyll": [avg("chlorophyll", d) for d in timestamps],
#     })


# def _temporal_from_sqlite(plant_id, camera, days):
#     """Fallback: build temporal response from local SQLite PlantTraits."""

#     qs = (
#         PlantTraits.objects.select_related("image")
#         .filter(image__plant_id=plant_id)
#     )
#     if camera:
#         qs = qs.filter(image__camera=camera)

#     last_dates = list(
#         qs.values_list("image__date_folder", flat=True)
#         .distinct()
#         .order_by("-image__date_folder")[:days]
#     )

#     if not last_dates:
#         return _empty_temporal(plant_id, camera, days)

#     qs = qs.filter(image__date_folder__in=last_dates)

#     sums = defaultdict(float)
#     cnts = defaultdict(int)
#     sums_chlorosis   = defaultdict(float); cnts_chlorosis   = defaultdict(int)
#     sums_vigor       = defaultdict(float); cnts_vigor       = defaultdict(int)
#     sums_chlorophyll = defaultdict(float); cnts_chlorophyll = defaultdict(int)

#     for obj in qs:
#         d = obj.image.date_folder
#         t = obj.traits or {}

#         v = _get_float_nested(t, ["plant", "health_score"])
#         if v is not None:
#             sums[d] += v; cnts[d] += 1

#         v = _get_float_nested(t, ["plant", "chlorosis_pct"])
#         if v is not None:
#             sums_chlorosis[d] += v; cnts_chlorosis[d] += 1

#         v = _get_float_nested(t, ["plant", "vigor_pct"])
#         if v is not None:
#             sums_vigor[d] += v; cnts_vigor[d] += 1

#         v = _get_float_nested(t, ["plant", "chlorophyll_level"])
#         if v is not None:
#             sums_chlorophyll[d] += v; cnts_chlorophyll[d] += 1

#     timestamps = sorted(last_dates)

#     def avg(d, s, c):
#         n = c.get(d, 0)
#         return (s[d] / n) if n else None

#     return Response({
#         "plant_id":   plant_id,
#         "camera":     camera,
#         "range_days": days,
#         "timestamps": timestamps,
#         "health":      [avg(d, sums,             cnts)             for d in timestamps],
#         "chlorosis":   [avg(d, sums_chlorosis,   cnts_chlorosis)   for d in timestamps],
#         "vigor":       [avg(d, sums_vigor,        cnts_vigor)       for d in timestamps],
#         "chlorophyll": [avg(d, sums_chlorophyll, cnts_chlorophyll) for d in timestamps],
#     })


# def _empty_temporal(plant_id, camera, days):
#     return Response({
#         "plant_id":   plant_id,
#         "camera":     camera,
#         "range_days": days,
#         "timestamps": [],
#         "health":      [],
#         "chlorosis":   [],
#         "vigor":       [],
#         "chlorophyll": [],
#     })


# # ─────────────────────────────────────────────────────────────────────────────
# # Leaf segments endpoint — unchanged, reads from local filesystem
# # ─────────────────────────────────────────────────────────────────────────────

# @api_view(["GET"])
# def image_leaf_segments(request, image_id: int):
#     """
#     GET /api/images/<image_id>/leaves/
#     Returns segmented leaf images + per-leaf traits computed on the fly.
#     """
#     try:
#         img = PlantImage.objects.get(id=image_id)
#     except PlantImage.DoesNotExist:
#         return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

#     media_root = Path(settings.MEDIA_ROOT)

#     seg_rel = Path("segmented") / Path(img.rel_path).with_suffix("")
#     seg_dir = media_root / seg_rel

#     leaves = []

#     if seg_dir.exists():
#         leaf_files = sorted(seg_dir.glob("masked_object_*.png"))

#         for i, lf in enumerate(leaf_files):
#             leaf_rel = str(lf.relative_to(media_root))
#             leaf_url = request.build_absolute_uri("/media/" + leaf_rel)
#             leaf_traits = _compute_single_leaf_traits(lf)
#             leaves.append({
#                 "index":     i,
#                 "image_url": leaf_url,
#                 "traits":    leaf_traits,
#             })

#     return Response({
#         "image_id":   image_id,
#         "leaf_count": len(leaves),
#         "leaves":     leaves,
#     })


# def _compute_single_leaf_traits(leaf_path: Path) -> dict:
#     """Compute traits for one segmented leaf PNG."""
#     import cv2
#     import numpy as np

#     leaf = cv2.imread(str(leaf_path))
#     if leaf is None:
#         return {}

#     gray = cv2.cvtColor(leaf, cv2.COLOR_BGR2GRAY)
#     _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)

#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     if not contours:
#         return {
#             "leaf_area_px": 0, "aspect_ratio": 0, "solidity": 0,
#             "vigor_pct": 0, "average_color_uniformity_pct": 0,
#             "chlorophyll_level": 0, "texture_entropy": 0,
#             "chlorosis_pct": 0, "health_score": 0,
#         }

#     cnt  = max(contours, key=cv2.contourArea)
#     area = float(cv2.contourArea(cnt))
#     rect = cv2.minAreaRect(cnt)
#     w, h = rect[1]
#     aspect_ratio = float(max(w, h) / min(w, h)) if w and h else 0.0
#     hull      = cv2.convexHull(cnt)
#     hull_area = float(cv2.contourArea(hull))
#     solidity  = float(area / hull_area) if hull_area > 0 else 0.0

#     m = mask > 0
#     if not np.any(m):
#         return {
#             "leaf_area_px": area, "aspect_ratio": aspect_ratio,
#             "solidity": solidity, "vigor_pct": 0,
#             "average_color_uniformity_pct": 0, "chlorophyll_level": 0,
#             "texture_entropy": 0, "chlorosis_pct": 0, "health_score": 0,
#         }

#     hsv      = cv2.cvtColor(leaf, cv2.COLOR_BGR2HSV)
#     lab      = cv2.cvtColor(leaf, cv2.COLOR_BGR2LAB)
#     gray_img = cv2.cvtColor(leaf, cv2.COLOR_BGR2GRAY)

#     h_ch, s_ch, _ = cv2.split(hsv)
#     _, a_ch, _    = cv2.split(lab)

#     hue_std         = float(np.std(h_ch[m]))
#     color_uniformity = float(np.clip(1.0 - (hue_std / 180.0), 0.0, 1.0)) * 100.0
#     vigor            = float(np.clip(np.mean(s_ch[m]) / 255.0, 0.0, 1.0)) * 100.0
#     chlorophyll_raw  = -float(np.mean(a_ch[m]))
#     chlorophyll      = float(np.clip((chlorophyll_raw + 128.0) / 255.0, 0.0, 1.0))

#     vals = gray_img[m]
#     hist = np.bincount(vals, minlength=256).astype(np.float64)
#     hist = hist / (hist.sum() + 1e-9)
#     ent  = -np.sum(hist * np.log2(hist + 1e-12)) / 8.0
#     texture_entropy = float(np.clip(ent, 0.0, 1.0))

#     mask01      = (mask > 0).astype(np.uint8)
#     total_leaf  = float(np.sum(mask01))
#     hsv_masked  = cv2.bitwise_and(hsv, hsv, mask=mask01)
#     yellow      = cv2.inRange(hsv_masked, (25, 50, 50), (40, 255, 255))
#     chlorosis_area = float(np.sum((yellow > 0) & (mask01 > 0)))
#     chlorosis_pct  = float(min(100.0, (chlorosis_area / total_leaf) * 100.0)) if total_leaf > 0 else 0.0
#     health_score   = float(np.clip(100.0 - chlorosis_pct, 0.0, 100.0))

#     return {
#         "leaf_area_px":                 round(area, 1),
#         "aspect_ratio":                 round(aspect_ratio, 2),
#         "solidity":                     round(solidity, 3),
#         "vigor_pct":                    round(vigor, 1),
#         "average_color_uniformity_pct": round(color_uniformity, 1),
#         "chlorophyll_level":            round(chlorophyll, 3),
#         "texture_entropy":              round(texture_entropy, 3),
#         "chlorosis_pct":                round(chlorosis_pct, 1),
#         "health_score":                 round(health_score, 1),
#     }
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PlantImage, PlantTraits
from .serializers import PlantImageSerializer, PlantTraitsSerializer


@api_view(["GET"])
def list_images(request):
    """
    GET /api/images/
    GET /api/images/?plant_id=1
    GET /api/images/?plant_id=1&camera=CAM2
    GET /api/images/?plant_id=1&camera=CAM2&date=2025-02-10
    """
    plant_id = request.GET.get("plant_id")
    camera   = request.GET.get("camera")
    date     = request.GET.get("date")

    qs = PlantImage.objects.all().order_by("-date_folder", "camera", "filename")

    if plant_id:
        qs = qs.filter(plant_id=plant_id)
    if camera:
        qs = qs.filter(camera=camera)
    if date:
        qs = qs.filter(date_folder=date)

    data = PlantImageSerializer(qs, many=True).data

    for row in data:
        row["image_url"] = request.build_absolute_uri("/media/" + row["rel_path"])

    return Response(data)


@api_view(["GET"])
def image_filters(request):
    """
    GET /api/filters/

    Returns all available cameras and dates so the frontend
    can populate the camera dropdown and date slider dynamically.

    Response:
    {
        "cameras": ["CAM1", "CAM2", "CAM3"],
        "dates": ["2025-01-09", "2025-01-10", ..., "2025-03-02"]
    }
    """
    plant_id = request.GET.get("plant_id")

    qs = PlantImage.objects.all()
    if plant_id:
        qs = qs.filter(plant_id=plant_id)

    cameras = sorted(
        qs.values_list("camera", flat=True).distinct()
    )

    dates = sorted(
        qs.values_list("date_folder", flat=True).distinct()
    )

    return Response({
        "cameras": cameras,
        "dates":   dates,
    })


@api_view(["GET"])
def image_traits(request, image_id: int):
    """
    GET /api/images/<image_id>/traits/
    """
    try:
        obj = PlantTraits.objects.get(image_id=image_id)
    except PlantTraits.DoesNotExist:
        return Response({"detail": "Traits not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(PlantTraitsSerializer(obj).data)


def _get_float_nested(d: dict, keys: list[str]):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur.get(k)
    if cur is None:
        return None
    try:
        return float(cur)
    except (TypeError, ValueError):
        return None


@api_view(["GET"])
def plant_temporal(request):
    """
    GET /api/traits/temporal/?plant_id=1&days=30&camera=CAM2
    """
    plant_id = request.GET.get("plant_id")
    camera   = request.GET.get("camera")
    days     = request.GET.get("days", "7")

    if not plant_id:
        return Response({"detail": "plant_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        plant_id = int(plant_id)
    except ValueError:
        return Response({"detail": "plant_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        days = int(days)
    except ValueError:
        return Response({"detail": "days must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    qs = (
        PlantTraits.objects.select_related("image")
        .filter(image__plant_id=plant_id)
    )
    if camera:
        qs = qs.filter(image__camera=camera)

    last_dates = list(
        qs.values_list("image__date_folder", flat=True)
        .distinct()
        .order_by("-image__date_folder")[:days]
    )

    if not last_dates:
        return Response({
            "plant_id":   plant_id,
            "camera":     camera,
            "range_days": days,
            "timestamps": [],
            "health":      [],
            "chlorosis":   [],
            "vigor":       [],
            "chlorophyll": [],
        })

    qs = qs.filter(image__date_folder__in=last_dates)

    sums             = defaultdict(float); cnts             = defaultdict(int)
    sums_chlorosis   = defaultdict(float); cnts_chlorosis   = defaultdict(int)
    sums_vigor       = defaultdict(float); cnts_vigor       = defaultdict(int)
    sums_chlorophyll = defaultdict(float); cnts_chlorophyll = defaultdict(int)

    for obj in qs:
        d = obj.image.date_folder
        t = obj.traits or {}

        v = _get_float_nested(t, ["plant", "health_score"])
        if v is not None:
            sums[d] += v; cnts[d] += 1

        v = _get_float_nested(t, ["plant", "chlorosis_pct"])
        if v is not None:
            sums_chlorosis[d] += v; cnts_chlorosis[d] += 1

        v = _get_float_nested(t, ["plant", "vigor_pct"])
        if v is not None:
            sums_vigor[d] += v; cnts_vigor[d] += 1

        v = _get_float_nested(t, ["plant", "chlorophyll_level"])
        if v is not None:
            sums_chlorophyll[d] += v; cnts_chlorophyll[d] += 1

    timestamps = sorted(last_dates)

    def avg(d, s, c):
        n = c.get(d, 0)
        return (s[d] / n) if n else None

    return Response({
        "plant_id":   plant_id,
        "camera":     camera,
        "range_days": days,
        "timestamps": timestamps,
        "health":      [avg(d, sums,             cnts)             for d in timestamps],
        "chlorosis":   [avg(d, sums_chlorosis,   cnts_chlorosis)   for d in timestamps],
        "vigor":       [avg(d, sums_vigor,        cnts_vigor)       for d in timestamps],
        "chlorophyll": [avg(d, sums_chlorophyll, cnts_chlorophyll) for d in timestamps],
    })


# ─────────────────────────────────────────────────────────────────────────────
# Leaf segments — reads from local filesystem
# ─────────────────────────────────────────────────────────────────────────────

@api_view(["GET"])
def image_leaf_segments(request, image_id: int):
    """
    GET /api/images/<image_id>/leaves/
    """
    try:
        img = PlantImage.objects.get(id=image_id)
    except PlantImage.DoesNotExist:
        return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    media_root = Path(settings.MEDIA_ROOT)
    seg_rel    = Path("segmented") / Path(img.rel_path).with_suffix("")
    seg_dir    = media_root / seg_rel
    leaves     = []

    if seg_dir.exists():
        for i, lf in enumerate(sorted(seg_dir.glob("masked_object_*.png"))):
            leaf_rel = str(lf.relative_to(media_root))
            leaf_url = request.build_absolute_uri("/media/" + leaf_rel)
            leaves.append({
                "index":     i,
                "image_url": leaf_url,
                "traits":    _compute_single_leaf_traits(lf),
            })

    return Response({
        "image_id":   image_id,
        "leaf_count": len(leaves),
        "leaves":     leaves,
    })


def _compute_single_leaf_traits(leaf_path: Path) -> dict:
    import cv2
    import numpy as np

    leaf = cv2.imread(str(leaf_path))
    if leaf is None:
        return {}

    gray = cv2.cvtColor(leaf, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return {
            "leaf_area_px": 0, "aspect_ratio": 0, "solidity": 0,
            "vigor_pct": 0, "average_color_uniformity_pct": 0,
            "chlorophyll_level": 0, "texture_entropy": 0,
            "chlorosis_pct": 0, "health_score": 0,
        }

    cnt       = max(contours, key=cv2.contourArea)
    area      = float(cv2.contourArea(cnt))
    rect      = cv2.minAreaRect(cnt)
    w, h      = rect[1]
    aspect_ratio = float(max(w, h) / min(w, h)) if w and h else 0.0
    hull      = cv2.convexHull(cnt)
    hull_area = float(cv2.contourArea(hull))
    solidity  = float(area / hull_area) if hull_area > 0 else 0.0

    m = mask > 0
    if not np.any(m):
        return {
            "leaf_area_px": area, "aspect_ratio": aspect_ratio, "solidity": solidity,
            "vigor_pct": 0, "average_color_uniformity_pct": 0,
            "chlorophyll_level": 0, "texture_entropy": 0,
            "chlorosis_pct": 0, "health_score": 0,
        }

    hsv      = cv2.cvtColor(leaf, cv2.COLOR_BGR2HSV)
    lab      = cv2.cvtColor(leaf, cv2.COLOR_BGR2LAB)
    gray_img = cv2.cvtColor(leaf, cv2.COLOR_BGR2GRAY)
    h_ch, s_ch, _ = cv2.split(hsv)
    _, a_ch, _    = cv2.split(lab)

    color_uniformity = float(np.clip(1.0 - (float(np.std(h_ch[m])) / 180.0), 0.0, 1.0)) * 100.0
    vigor            = float(np.clip(np.mean(s_ch[m]) / 255.0, 0.0, 1.0)) * 100.0
    chlorophyll      = float(np.clip((-float(np.mean(a_ch[m])) + 128.0) / 255.0, 0.0, 1.0))

    vals = gray_img[m]
    hist = np.bincount(vals, minlength=256).astype(np.float64)
    hist = hist / (hist.sum() + 1e-9)
    texture_entropy = float(np.clip(-np.sum(hist * np.log2(hist + 1e-12)) / 8.0, 0.0, 1.0))

    mask01         = (mask > 0).astype(np.uint8)
    total_leaf     = float(np.sum(mask01))
    hsv_masked     = cv2.bitwise_and(hsv, hsv, mask=mask01)
    yellow         = cv2.inRange(hsv_masked, (25, 50, 50), (40, 255, 255))
    chlorosis_area = float(np.sum((yellow > 0) & (mask01 > 0)))
    chlorosis_pct  = float(min(100.0, (chlorosis_area / total_leaf) * 100.0)) if total_leaf > 0 else 0.0

    return {
        "leaf_area_px":                 round(area, 1),
        "aspect_ratio":                 round(aspect_ratio, 2),
        "solidity":                     round(solidity, 3),
        "vigor_pct":                    round(vigor, 1),
        "average_color_uniformity_pct": round(color_uniformity, 1),
        "chlorophyll_level":            round(chlorophyll, 3),
        "texture_entropy":              round(texture_entropy, 3),
        "chlorosis_pct":                round(chlorosis_pct, 1),
        "health_score":                 round(100.0 - chlorosis_pct, 1),
    }