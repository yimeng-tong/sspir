import argparse
import csv
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Aggregate metric summaries into markdown/csv tables.")
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--allowed-method", action="append", default=[])
    parser.add_argument("--only-completed", action="store_true")
    return parser.parse_args()


def format_metric(value):
    return f"{value:.4f}" if isinstance(value, (int, float)) else "NA"


def format_elapsed(value):
    return f"{value:.2f}" if isinstance(value, (int, float)) else "NA"


def main():
    args = parse_args()
    input_root = Path(args.input_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    allowed_methods = set(args.allowed_method)

    summary_files = sorted(input_root.rglob("summary.json"))
    if not summary_files:
        print(f"No summary.json files found under {input_root}")
        return

    rows = []
    for summary_file in summary_files:
        data = json.loads(summary_file.read_text(encoding="utf-8"))
        run_status = data.get("run_status", {})
        method = data.get("method")

        if allowed_methods and method not in allowed_methods:
            continue
        if args.only_completed and run_status.get("state") != "completed":
            continue

        rows.append(
            {
                "method": method,
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

    if not rows:
        print("No summary rows matched the requested filters.")
        return

    rows.sort(key=lambda row: (row["dataset_name"] or "", row["method"] or "", row["summary_path"]))

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
            "| {method} | {dataset_name} | {num_images} | {psnr_display} | {ssim_display} | {lpips_display} | {niqe_display} | {elapsed_display} |".format(
                method=row["method"],
                dataset_name=row["dataset_name"],
                num_images=row["num_images"],
                psnr_display=format_metric(row["psnr"]),
                ssim_display=format_metric(row["ssim"]),
                lpips_display=format_metric(row["lpips"]),
                niqe_display=format_metric(row["niqe"]),
                elapsed_display=format_elapsed(row["elapsed_sec"]),
            )
        )

    md_path = output_root / "aggregated_metrics.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
