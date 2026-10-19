# traits/engine_b/traits_from_segmented.py

from pathlib import Path
import cv2
import numpy as np


def binary_mask_from_segmented_leaf(leaf_bgr):
    """
    Segmented leaf is leaf on black background.
    Create binary mask from non-black pixels.
    """
    gray = cv2.cvtColor(leaf_bgr, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)
    return mask


def morph_from_mask(mask):
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return {
            "leaf_area_px": 0.0,
            "aspect_ratio": 0.0,
            "solidity": 0.0,
        }

    cnt = max(contours, key=cv2.contourArea)

    area = float(cv2.contourArea(cnt))

    rect = cv2.minAreaRect(cnt)
    w, h = rect[1]

    aspect_ratio = float(max(w, h) / min(w, h)) if w and h else 0.0

    hull = cv2.convexHull(cnt)
    hull_area = float(cv2.contourArea(hull))

    solidity = float(area / hull_area) if hull_area > 0 else 0.0

    return {
        "leaf_area_px": area,
        "aspect_ratio": aspect_ratio,
        "solidity": solidity,
    }


def color_vigor_chloro_entropy(leaf_bgr, mask):
    m = mask > 0
    if not np.any(m):
        return {
            "vigor_pct": 0.0,
            "average_color_uniformity_pct": 0.0,
            "chlorophyll_level": 0.0,
            "texture_entropy": 0.0,
            "chlorosis_pct": 0.0,
            "health_score": 0.0,
        }

    hsv = cv2.cvtColor(leaf_bgr, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(leaf_bgr, cv2.COLOR_BGR2LAB)
    gray = cv2.cvtColor(leaf_bgr, cv2.COLOR_BGR2GRAY)

    h, s, v = cv2.split(hsv)
    L, a, b = cv2.split(lab)

    # --- average_color_uniformity_pct (matches your V1/V2-style color_health) ---
    hue_std = float(np.std(h[m]))
    color_uniformity_pct = float(np.clip(1.0 - (hue_std / 180.0), 0.0, 1.0)) * 100.0

    # --- vigor_pct (V2-style) ---
    vigor_pct = float(np.clip(np.mean(s[m]) / 255.0, 0.0, 1.0)) * 100.0

    # --- chlorophyll_level (V2 EXACT) ---
    chlorophyll_raw = -float(np.mean(a[m]))
    chlorophyll_level = float(np.clip((chlorophyll_raw + 128.0) / 255.0, 0.0, 1.0))

    # --- texture_entropy (same as your V1 normalized entropy) ---
    vals = gray[m]
    hist = np.bincount(vals, minlength=256).astype(np.float64)
    hist = hist / (hist.sum() + 1e-9)
    ent = -np.sum(hist * np.log2(hist + 1e-12)) / 8.0
    texture_entropy = float(np.clip(ent, 0.0, 1.0))

    # ============================
    # CHLOROSIS (MATCH V2 EXACTLY)
    # ============================
    mask01 = (mask > 0).astype(np.uint8)
    total_leaf_area = float(np.sum(mask01))

    hsv_masked = cv2.bitwise_and(hsv, hsv, mask=mask01)
    yellow_stress = cv2.inRange(hsv_masked, (25, 50, 50), (40, 255, 255))

    chlorosis_area = float(np.sum((yellow_stress > 0) & (mask01 > 0)))
    chlorosis_pct = (chlorosis_area / total_leaf_area) * 100.0 if total_leaf_area > 0 else 0.0
    chlorosis_pct = float(min(100.0, chlorosis_pct))

    # health_score (since DB stores only chlorosis, keep this as 100 - chlorosis)
    health_score = float(np.clip(100.0 - chlorosis_pct, 0.0, 100.0))

    return {
        "vigor_pct": vigor_pct,
        "average_color_uniformity_pct": color_uniformity_pct,
        "chlorophyll_level": chlorophyll_level,
        "texture_entropy": texture_entropy,
        "chlorosis_pct": chlorosis_pct,
        "health_score": health_score,
    }


def compute_traits_from_segmented_dir(segmented_dir: Path) -> dict:
    leaf_files = sorted(
        segmented_dir.glob("masked_object_*.png")
    )

    if not leaf_files:
        return {
            "leaf_count": 0,
            "leaf_area_px": 0,
            "aspect_ratio": 0,
            "solidity": 0,
            "vigor_pct": 0,
            "average_color_uniformity_pct": 0,
            "chlorophyll_level": 0,
            "texture_entropy": 0,
            "chlorosis_pct": 0,
            "health_score": 0,
        }

    rows = []

    for lf in leaf_files:
        leaf = cv2.imread(str(lf))

        if leaf is None:
            continue

        mask = binary_mask_from_segmented_leaf(leaf)

        morph = morph_from_mask(mask)
        col = color_vigor_chloro_entropy(leaf, mask)

        rows.append({**morph, **col})

    if not rows:
        return {"leaf_count": 0}

    # ---------- Aggregate (mean) ----------
    def mean(k):
        vals = [r.get(k, 0) for r in rows]
        return float(np.mean(vals)) if vals else 0.0

    return {
        "leaf_count": len(rows),
        "leaf_area_px": mean("leaf_area_px"),
        "aspect_ratio": mean("aspect_ratio"),
        "solidity": mean("solidity"),
        "vigor_pct": mean("vigor_pct"),
        "average_color_uniformity_pct": mean("average_color_uniformity_pct"),
        "chlorophyll_level": mean("chlorophyll_level"),
        "texture_entropy": mean("texture_entropy"),
        "chlorosis_pct": mean("chlorosis_pct"),
        "health_score": mean("health_score"),
    }



def plant_mask_from_raw_image(raw_bgr: np.ndarray) -> np.ndarray:
    """
    Rough whole-plant mask from a RAW image using HSV green threshold.
    Returns 0/255 mask.
    """
    hsv = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2HSV)

    # Tune if needed (works decently for "green plant" cases)
    lower = np.array([25, 40, 40])   # H,S,V
    upper = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    # cleanup
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask



# def binary_mask_from_isolated_plant(plant_bgr):
#     """
#     Isolated plant is plant on black background.
#     Create binary mask from non-black pixels.
#     """
#     gray = cv2.cvtColor(plant_bgr, cv2.COLOR_BGR2GRAY)
#     _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)
#     return mask


def compute_plant_traits_from_raw_image(raw_path: Path) -> dict:
    raw = cv2.imread(str(raw_path))
    if raw is None:
        return {
            "leaf_area_px": 0,
            "aspect_ratio": 0,
            "solidity": 0,
            "vigor_pct": 0,
            "average_color_uniformity_pct": 0,
            "chlorophyll_level": 0,
            "texture_entropy": 0,
            "chlorosis_pct": 0,
            "health_score": 0,
        }

    mask = plant_mask_from_raw_image(raw)

    morph = morph_from_mask(mask)
    col = color_vigor_chloro_entropy(raw, mask)

    return {**morph, **col}