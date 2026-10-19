# traits/pipeline/segmenter.py

import os
import sys
from pathlib import Path
from typing import List

import cv2
import numpy as np
from PIL import Image
import torch
from torchvision.ops import box_convert


# ---------- device ----------
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["YOLO_DEVICE"] = "cpu"
os.environ["MPS_ENABLE"] = "1"

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"


# ---------- paths ----------
BASE_DIR = Path(__file__).resolve().parents[2]  # plant_backend/
THIRD = BASE_DIR / "third_party"

sys.path.append(str(THIRD / "GroundingDINO"))
sys.path.append(str(THIRD / "fastsam"))


from groundingdino.util.inference import load_model, load_image, predict


# Safe loader for FastSAM-x.pt on newer torch
def load_fastsam_safely(weights_path: str):
    # Torch 2.2.x does NOT need add_safe_globals
    from fastsam import FastSAM
    return FastSAM(weights_path)


GROUNDING_CONFIG = THIRD / "GroundingDINO" / "groundingdino" / "config" / "GroundingDINO_SwinT_OGC.py"
GROUNDING_WEIGHTS = THIRD / "weights" / "groundingdino_swint_ogc.pth"
FASTSAM_W = THIRD / "weights" / "FastSAM-x.pt"


model_dino = load_model(
    model_config_path=str(GROUNDING_CONFIG),
    model_checkpoint_path=str(GROUNDING_WEIGHTS),
)

model_sam = load_fastsam_safely(str(FASTSAM_W))


def get_bounding_box(image_path: Path) -> List[List[int]]:
    image_source, image = load_image(str(image_path))

    boxes, logits, phrases = predict(
        model=model_dino,
        image=image,
        caption="green plant only without soil",
        box_threshold=0.25,
        text_threshold=0.35,
        device="cpu",
    )

    if boxes is None or boxes.size(0) == 0:
        raise RuntimeError("No bounding boxes found")

    h, w = image_source.shape[:2]

    boxes_xyxy = box_convert(
        boxes,
        in_fmt="cxcywh",
        out_fmt="xyxy"
    ).cpu().numpy()

    boxes_xyxy[:, [0, 2]] *= w
    boxes_xyxy[:, [1, 3]] *= h

    boxes_xyxy = boxes_xyxy.astype(int).tolist()

    smallest = min(
        boxes_xyxy,
        key=lambda b: (b[2] - b[0]) * (b[3] - b[1])
    )

    return [smallest]


def remove_background(image_path: Path, bboxes: List[List[int]], output_path: Path):
    results = model_sam(
        str(image_path),
        device=DEVICE,
        retina_masks=True,
        imgsz=1024,
    )

    try:
        from fastsam import FastSAMPrompt
    except ImportError:
        from fastsam.prompt import FastSAMPrompt

    prompt = FastSAMPrompt(str(image_path), results, device=DEVICE)
    ann = prompt.box_prompt(bboxes=bboxes)

    mask = ann.squeeze().astype(np.uint8)

    original = cv2.imread(str(image_path))
    mask3 = cv2.merge([mask, mask, mask])

    isolated = original * mask3

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), isolated)

    return isolated


def _to_bool_np(mask):
    if torch.is_tensor(mask):
        return mask.detach().cpu().numpy().astype(bool)
    return np.asarray(mask).astype(bool)


def filter_masks(masks, original):
    gray = (
        cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        if original.ndim == 3
        else original
    )

    non_black = gray > 10  # tweak 5–20 if needed
    content_area = int(np.sum(non_black))

    valid = []

    for mask in masks:
        m = _to_bool_np(mask)
        area = np.sum(m)

        if 0.001 * content_area < area < 0.95 * content_area:
            overlap = np.logical_and(non_black, m)

            if np.sum(overlap) / content_area < 0.8:
                valid.append(mask)

    def iou(a, b):
        a = _to_bool_np(a)
        b = _to_bool_np(b)

        inter = np.logical_and(a, b)
        union = np.logical_or(a, b)

        return np.sum(inter) / np.sum(union)

    final = []

    for m in sorted(
        valid,
        key=lambda x: np.sum(_to_bool_np(x)),
        reverse=True
    ):
        if not any(iou(m, f) > 0.7 for f in final):
            final.append(m)

    return final


def segment_leaves(isolated_path: Path, seg_dir: Path) -> int:
    original = cv2.imread(str(isolated_path))
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    results = model_sam(
        str(isolated_path),
        device=DEVICE,
        retina_masks=True,
        imgsz=1024,
    )

    try:
        from fastsam import FastSAMPrompt
    except ImportError:
        from fastsam.prompt import FastSAMPrompt

    prompt = FastSAMPrompt(str(isolated_path), results, device=DEVICE)
    ann = prompt.everything_prompt()

    # --- normalize ann to list of 2D masks ---
    if torch.is_tensor(ann):

        if ann.ndim == 3:
            masks = [ann[i] for i in range(ann.shape[0])]
        elif ann.ndim == 2:
            masks = [ann]
        else:
            raise RuntimeError(
                f"Unexpected ann tensor shape: {tuple(ann.shape)}"
            )
    else:
        masks = ann

    if len(masks) == 1:
        filtered = masks
    else:
        filtered = filter_masks(masks, original)

    seg_dir.mkdir(parents=True, exist_ok=True)

    count = 0

    for i, mask in enumerate(filtered):

        if torch.is_tensor(mask):
            m = mask.detach().cpu().numpy()
        else:
            m = np.asarray(mask)

        m = m.astype(bool)

        out = np.zeros_like(original)
        out[m] = original[m]

        Image.fromarray(out).save(
            seg_dir / f"masked_object_{i}.png"
        )

        count += 1

    return count


def run_segmentation_for_image(image_abs_path: Path, media_root: Path) -> dict:
    """
    Input: absolute path to original image under MEDIA_ROOT
    Output: dict with isolated_path + segmented_dir + num_leaves
    """

    rel = image_abs_path.relative_to(media_root)

    isolated_path = media_root / "isolated" / rel
    segmented_dir = media_root / "segmented" / rel.with_suffix("")

    bbox = get_bounding_box(image_abs_path)

    remove_background(
        image_abs_path,
        bbox,
        isolated_path
    )

    count = segment_leaves(
        isolated_path,
        segmented_dir
    )

    return {
        "isolated_path": str(isolated_path),
        "segmented_dir": str(segmented_dir),
        "leaf_count": int(count),
    }