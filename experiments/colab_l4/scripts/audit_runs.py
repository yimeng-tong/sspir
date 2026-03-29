import argparse
import csv
import json
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp"}


def parse_args():
    parser = argparse.ArgumentParser(description="Audit completed LLIE runs and metric summaries.")
    parser.add_argument("--input-root", required=True, help="Root directory that contains method/dataset/run folders.")
    parser.add_argument("--output-root", required=True, help="Directory for audit csv/md outputs.")
    parser.add_argument("--only-completed", action="store_true", help="Only keep runs whose status.json state is completed.")
    return parser.parse_args()


def count_images(path_str: str) -> int:
    path = Path(path_str)
    if not path.exists():
        return 0
    return sum(1 for p in path.rglob("*") if p.suffix.lower() in IMAGE_EXTS)


def main():
    args = parse_args()
    input_root = Path(args.input_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    rows = []
    for meta_path in sorted(input_root.rglob("run_metadata.json")):
        run_dir = meta_path.parent
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

        status_path = Path(meta.get("status_path", "")) if meta.get("status_path") else run_dir / "status.json"
        status = {}
        if status_path.exists():
            status = json.loads(status_path.read_text(encoding="utf-8"))

        state = status.get("state", "missing")
        if args.only_completed and state != "completed":
            continue

        pred_dir = Path(meta.get("pred_dir", ""))
        pred_image_count = count_images(str(pred_dir)) if pred_dir else 0

        summary_path = run_dir / "metrics" / "summary.json"
        summary = {}
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))

        rows.append(
            {
                "method": meta.get("method"),
                "dataset_name": meta.get("dataset_name"),
                "run_dir": str(run_dir),
                "state": state,
                "elapsed_sec": status.get("elapsed_sec"),
                "pred_dir": str(pred_dir),
                "pred_image_count": pred_image_count,
                "has_summary": summary_path.exists(),
                "summary_num_images": summary.get("num_images"),
                "summary_psnr": summary.get("psnr"),
                "summary_ssim": summary.get("ssim"),
                "summary_lpips": summary.get("lpips"),
                "summary_niqe": summary.get("niqe"),
                "summary_path": str(summary_path) if summary_path.exists() else "",
            }
        )

    csv_path = output_root / "audit_runs.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "method",
                "dataset_name",
                "run_dir",
                "state",
                "elapsed_sec",
                "pred_dir",
                "pred_image_count",
                "has_summary",
                "summary_num_images",
                "summary_psnr",
                "summary_ssim",
                "summary_lpips",
                "summary_niqe",
                "summary_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "# Run Audit",
        "",
        "| Method | Dataset | State | Pred Images | Has Summary | Summary Images | PSNR | SSIM | LPIPS |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        md_lines.append(
            "| {method} | {dataset_name} | {state} | {pred_image_count} | {has_summary} | {summary_num_images} | {summary_psnr} | {summary_ssim} | {summary_lpips} |".format(
                method=row["method"],
                dataset_name=row["dataset_name"],
                state=row["state"],
                pred_image_count=row["pred_image_count"],
                has_summary="yes" if row["has_summary"] else "no",
                summary_num_images=row["summary_num_images"] if row["summary_num_images"] is not None else "NA",
                summary_psnr=f'{row["summary_psnr"]:.4f}' if isinstance(row["summary_psnr"], (int, float)) else "NA",
                summary_ssim=f'{row["summary_ssim"]:.4f}' if isinstance(row["summary_ssim"], (int, float)) else "NA",
                summary_lpips=f'{row["summary_lpips"]:.4f}' if isinstance(row["summary_lpips"], (int, float)) else "NA",
            )
        )

    md_path = output_root / "audit_runs.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
