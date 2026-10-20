import cv2
import numpy as np
from scipy.stats import entropy as scipy_entropy


def make_leaf_mask(image_bgr: np.ndarray) -> np.ndarray:
    """
    Very simple mask:
    - converts to HSV and keeps 'green-ish' pixels
    - returns binary mask (0/255)
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Tune these if needed
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    # cleanup
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask


def morphological_traits(mask: np.ndarray) -> dict:
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return {
            "leaf_area_px": 0.0,
            "leaf_count": 0,
            "aspect_ratio": 0.0,
            "solidity": 0.0,
        }

    # leaf count (rough): number of connected blobs
    num_labels, labels = cv2.connectedComponents(
        (mask > 0).astype(np.uint8)
    )

    leaf_count = max(0, num_labels - 1)  # exclude background

    # largest contour = dominant leaf region
    cnt = max(contours, key=cv2.contourArea)
    area = float(cv2.contourArea(cnt))

    rect = cv2.minAreaRect(cnt)
    w, h = rect[1]

    if w == 0 or h == 0:
        aspect_ratio = 0.0
    else:
        aspect_ratio = float(max(w, h) / min(w, h))

    hull = cv2.convexHull(cnt)
    hull_area = float(cv2.contourArea(hull))

    solidity = float(area / hull_area) if hull_area > 0 else 0.0

    return {
        "leaf_area_px": area,
        "leaf_count": int(leaf_count),
        "aspect_ratio": aspect_ratio,
        "solidity": solidity,
    }


def color_traits(image_bgr: np.ndarray, mask: np.ndarray) -> dict:
    m = mask > 0
    if not np.any(m):
        return {
            "color_uniformity": 0.0,
            "vigor": 0.0,
            "chlorophyll_level": 0.0,
            "texture_entropy": 0.0,
        }

    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    h, s, v = cv2.split(hsv)
    L, a, b = cv2.split(lab)

    # --- V2 exact color_uniformity ---
    hsv_std = np.std(hsv[m], axis=0)  # std for H,S,V
    color_uniformity = float(np.clip(1.0 - (float(np.mean(hsv_std)) / 255.0), 0.0, 1.0))

    # vigor (V1/V2 both use mean saturation / 255)
    vigor = float(np.clip(np.mean(s[m]) / 255.0, 0.0, 1.0))

    # chlorophyll (V2 logic)
    chlorophyll_raw = -float(np.mean(a[m]))
    chlorophyll_level = float(np.clip((chlorophyll_raw + 128.0) / 255.0, 0.0, 1.0))

    # texture entropy (V1-style normalized entropy)
    vals = gray[m]
    hist = np.bincount(vals, minlength=256).astype(np.float64)
    hist = hist / (hist.sum() + 1e-9)
    texture_entropy = float(scipy_entropy(hist + 1e-12, base=2) / 8.0)

    return {
        "color_uniformity": color_uniformity,
        "vigor": vigor,
        "chlorophyll_level": chlorophyll_level,
        "texture_entropy": texture_entropy,
    }


def stress_traits(image_bgr: np.ndarray, mask: np.ndarray) -> dict:
    m = mask > 0
    leaf_area = float(np.sum(m))
    if leaf_area == 0:
        return {"chlorosis_pct": 0.0, "health_score": 0.0}

    mask01 = (mask > 0).astype(np.uint8)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    hsv_masked = cv2.bitwise_and(hsv, hsv, mask=mask01)

    # --- V2 exact chlorosis (yellow_stress) ---
    yellow = cv2.inRange(hsv_masked, (25, 50, 50), (40, 255, 255))
    chlorosis_area = float(np.sum((yellow > 0) & (mask01 > 0)))
    chlorosis_pct = float(np.clip((chlorosis_area / leaf_area) * 100.0, 0.0, 100.0))

    # --- V2 exact health_score (healthy_green fraction), scaled to 0..100 ---
    healthy_green = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    num = float(np.sum((healthy_green > 0) & (mask01 > 0)))
    den = float(np.sum(mask01 > 0))
    health_score = float((num / den) * 100.0) if den > 0 else 0.0

    return {"chlorosis_pct": chlorosis_pct, "health_score": health_score}


def compute_traits_for_image(image_path: str) -> dict:
    image = cv2.imread(image_path)

    if image is None:
        return {"error": f"Could not read image: {image_path}"}

    mask = make_leaf_mask(image)

    morph = morphological_traits(mask)
    color = color_traits(image, mask)
    stress = stress_traits(image, mask)

    # Pack exactly how your frontend likes it (numbers + %)
    traits = {
        # top cards style
        "health_score": stress["health_score"],                          # 0..100
        "average_color_uniformity_pct": color["color_uniformity"] * 100.0,  # 0..100
        "chlorosis_pct": stress["chlorosis_pct"],                        # 0..100
        "vigor_pct": color["vigor"] * 100.0,                             # 0..100

        # other cards
        "leaf_count": morph["leaf_count"],
        "leaf_area_px": morph["leaf_area_px"],
        "texture_entropy": color["texture_entropy"],                     # 0..1
        "chlorophyll_level": color["chlorophyll_level"],                 # 0..1
        "aspect_ratio": morph["aspect_ratio"],
        "solidity": morph["solidity"],
    }

    return traits