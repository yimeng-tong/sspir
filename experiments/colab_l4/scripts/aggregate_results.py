import argparse
import csv
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Aggregate metric summaries into markdown/csv tables.")
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    input_root = Path(args.input_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    summary_files = sorted(input_root.rglob("summary.json"))
    if not summary_files:
        raise ValueError(f"No summary.json files found under {input_root}")

    rows = []
    for summary_file in summary_files:
        data = json.loads(summary_file.read_text(encoding="utf-8"))
        run_status = data.get("run_status", {})
        rows.append(
            {
                "method": data.get("method"),
                "dataset_name": data.get("dataset_name"),
                "num_images": data.get("num_images"),
                "psnr": data.get("psnr"),
                "ssim": data.get("ssim"),
                "lpips": data.get("lpips"),
                "niqe": data.get("niqe"),
                "elapsed_sec": run_status.get("elapsed_sec"),
                "pred_dir": data.get("pred_dir"),
                "summary_path": str(summary_file),
            }
        )

    csv_path = output_root / "aggregated_metrics.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "method",
                "dataset_name",
                "num_images",
                "psnr",
                "ssim",
                "lpips",
                "niqe",
                "elapsed_sec",
                "pred_dir",
                "summary_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "# Aggregated LLIE Results",
        "",
        "| Method | Dataset | Images | PSNR | SSIM | LPIPS | NIQE | Elapsed(s) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        md_lines.append(
            "| {method} | {dataset_name} | {num_images} | {psnr:.4f} | {ssim:.4f} | {lpips:.4f} | {niqe_display} | {elapsed_display} |".format(
                method=row["method"],
                dataset_name=row["dataset_name"],
                num_images=row["num_images"],
                psnr=row["psnr"],
                ssim=row["ssim"],
                lpips=row["lpips"],
                niqe_display=f"{row['niqe']:.4f}" if isinstance(row["niqe"], (int, float)) else "NA",
                elapsed_display=f"{row['elapsed_sec']:.2f}" if isinstance(row["elapsed_sec"], (int, float)) else "NA",
            )
        )

    md_path = output_root / "aggregated_metrics.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
