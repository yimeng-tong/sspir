import argparse
import csv
import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def parse_args():
    parser = argparse.ArgumentParser(description="Compute LLIE metrics for one prediction directory.")
    parser.add_argument("--method", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--pred-dir", required=True)
    parser.add_argument("--gt-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--status-path", default="")
    parser.add_argument("--strip-suffix", action="append", default=[])
    parser.add_argument("--use-niqe", action="store_true")
    parser.add_argument("--resize-pred-to-gt", action="store_true")
    return parser.parse_args()


def normalized_stem(path: Path, suffixes):
    stem = path.stem
    for suffix in suffixes:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem


def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"))


def to_tensor_uint8(img: np.ndarray) -> torch.Tensor:
    tensor = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
    return tensor.unsqueeze(0) * 2.0 - 1.0


def main():
    args = parse_args()
    pred_dir = Path(args.pred_dir)
    gt_dir = Path(args.gt_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pred_files = sorted([p for p in pred_dir.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp"}])
    gt_files = {p.stem: p for p in gt_dir.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp"}}

    if not pred_files:
        raise ValueError(f"No prediction images found in {pred_dir}")

    import lpips

    lpips_metric = lpips.LPIPS(net="alex")
    lpips_metric.eval()

    niqe_metric = None
    if args.use_niqe:
        try:
            import pyiqa

            niqe_metric = pyiqa.create_metric("niqe", device="cpu")
        except Exception as exc:
            print(f"NIQE disabled because pyiqa is unavailable: {exc}")

    rows = []
    for pred_path in pred_files:
        key = normalized_stem(pred_path, args.strip_suffix)
        gt_path = gt_files.get(key)
        if gt_path is None:
            print(f"Skip unmatched prediction: {pred_path.name}")
            continue

        pred = load_rgb(pred_path)
        gt = load_rgb(gt_path)
        if pred.shape != gt.shape:
            if args.resize_pred_to_gt:
                pred = np.array(Image.fromarray(pred).resize((gt.shape[1], gt.shape[0]), Image.BICUBIC))
            else:
                print(f"Skip size mismatch: {pred_path.name} pred={pred.shape} gt={gt.shape}")
                continue

        psnr = peak_signal_noise_ratio(gt, pred, data_range=255)
        ssim = structural_similarity(gt, pred, channel_axis=2, data_range=255)
        with torch.no_grad():
            lpips_value = float(lpips_metric(to_tensor_uint8(pred), to_tensor_uint8(gt)).item())

        niqe_value = None
        if niqe_metric is not None:
            with torch.no_grad():
                pred_tensor = torch.from_numpy(pred).permute(2, 0, 1).float().unsqueeze(0) / 255.0
                niqe_value = float(niqe_metric(pred_tensor).item())

        rows.append(
            {
                "image": key,
                "pred_name": pred_path.name,
                "gt_name": gt_path.name,
                "psnr": psnr,
                "ssim": ssim,
                "lpips": lpips_value,
                "niqe": niqe_value,
            }
        )

    if not rows:
        raise ValueError("No matched prediction/ground-truth pairs were found.")

    per_image_csv = output_dir / "per_image.csv"
    with per_image_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["image", "pred_name", "gt_name", "psnr", "ssim", "lpips", "niqe"])
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "method": args.method,
        "dataset_name": args.dataset_name,
        "num_images": len(rows),
        "pred_dir": str(pred_dir),
        "gt_dir": str(gt_dir),
        "psnr": float(np.mean([row["psnr"] for row in rows])),
        "ssim": float(np.mean([row["ssim"] for row in rows])),
        "lpips": float(np.mean([row["lpips"] for row in rows])),
        "niqe": None,
        "status_path": args.status_path or None,
    }
    niqe_values = [row["niqe"] for row in rows if row["niqe"] is not None]
    if niqe_values:
        summary["niqe"] = float(np.mean(niqe_values))

    if args.status_path:
        status_path = Path(args.status_path)
        if status_path.exists():
            summary["run_status"] = json.loads(status_path.read_text(encoding="utf-8"))

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
