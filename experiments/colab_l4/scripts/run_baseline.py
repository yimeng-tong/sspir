import argparse
import json
import shutil
import sys
import time
from pathlib import Path

import yaml

from progress_utils import (
    ensure_dir,
    read_json_with_comments,
    run_command,
    symlink_or_copy,
    update_status,
    write_json,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Run LLIE baseline inference in Colab.")
    parser.add_argument("--method", required=True, choices=["uretinex", "diff-retinex", "reti-diff"])
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--lq-dir", required=True)
    parser.add_argument("--gt-dir", required=True)
    parser.add_argument("--run-name", default="")
    parser.add_argument("--gpu-id", type=int, default=0)
    parser.add_argument("--python-bin", default=sys.executable)
    parser.add_argument("--use-gtmeans", action="store_true")

    parser.add_argument("--diff-tdn-weight", default="")
    parser.add_argument("--diff-rda-weight", default="")
    parser.add_argument("--diff-ida-weight", default="")

    parser.add_argument("--reti-template", default="")
    parser.add_argument("--reti-weight", default="")
    parser.add_argument("--reti-decom-weight", default="")

    return parser.parse_args()


def make_run_dir(output_root: Path, method: str, dataset_name: str, run_name: str) -> Path:
    suffix = run_name or time.strftime("%Y%m%d_%H%M%S")
    return output_root / method / dataset_name / suffix


def run_uretinex(args, run_dir: Path):
    repo_root = Path(args.repo_root)
    pred_dir = ensure_dir(run_dir / "predictions")
    status_path = run_dir / "status.json"
    cmd = [
        args.python_bin,
        "evaluate.py",
        "--low_dir",
        args.lq_dir,
        "--high_dir",
        args.gt_dir,
        "--output",
        str(pred_dir),
        "--gpu_id",
        str(args.gpu_id),
    ]
    code = run_command(cmd, repo_root, run_dir / "run.log", status_path)
    metadata = {
        "method": "uretinex",
        "dataset_name": args.dataset_name,
        "pred_dir": str(pred_dir),
        "gt_dir": args.gt_dir,
        "status_path": str(status_path),
    }
    write_json(run_dir / "run_metadata.json", metadata)
    return code, metadata


def run_diff_retinex(args, run_dir: Path):
    repo_root = Path(args.repo_root)
    status_path = run_dir / "status.json"
    pred_dir = ensure_dir(run_dir / "predictions")
    config_dir = ensure_dir(run_dir / "generated_configs")
    dataset_view = ensure_dir(run_dir / "dataset_view")

    symlink_or_copy(Path(args.lq_dir), dataset_view / "low")
    symlink_or_copy(Path(args.gt_dir), dataset_view / "high")

    if not args.diff_tdn_weight or not args.diff_rda_weight or not args.diff_ida_weight:
        raise ValueError("diff-retinex requires --diff-tdn-weight, --diff-rda-weight and --diff-ida-weight")

    symlink_or_copy(Path(args.diff_tdn_weight), repo_root / "model" / "Diff_TDN" / "weights" / "checkpoint_LOL_Diff_TDN.pth")

    main_cfg = read_json_with_comments(repo_root / "config" / "Diff_Retinex_val.json")
    rda_cfg = read_json_with_comments(repo_root / "model" / "Diff_RDA" / "config" / "Diff_RDA_data_val.json")
    ida_cfg = read_json_with_comments(repo_root / "model" / "Diff_IDA" / "config" / "Diff_IDA_data_val.json")

    main_cfg["name"] = f"Diff_Retinex_{args.dataset_name}"
    main_cfg["datasets"]["val"]["dataroot"] = str(dataset_view)
    main_cfg["path"]["log"] = str(run_dir / "logs")
    main_cfg["path"]["tb_logger"] = str(run_dir / "tb_logger")
    main_cfg["path"]["results"] = str(pred_dir)
    main_cfg["path"]["checkpoint"] = str(run_dir / "checkpoint")

    rda_cfg["name"] = f"Diff_RDA_{args.dataset_name}"
    rda_cfg["path"]["log"] = str(run_dir / "rda_logs")
    rda_cfg["path"]["tb_logger"] = str(run_dir / "rda_tb_logger")
    rda_cfg["path"]["results"] = str(run_dir / "rda_results")
    rda_cfg["path"]["checkpoint"] = str(run_dir / "rda_checkpoint")
    rda_cfg["path"]["resume_state"] = str(Path(args.diff_rda_weight))

    ida_cfg["name"] = f"Diff_IDA_{args.dataset_name}"
    ida_cfg["path"]["log"] = str(run_dir / "ida_logs")
    ida_cfg["path"]["tb_logger"] = str(run_dir / "ida_tb_logger")
    ida_cfg["path"]["results"] = str(run_dir / "ida_results")
    ida_cfg["path"]["checkpoint"] = str(run_dir / "ida_checkpoint")
    ida_cfg["path"]["resume_state"] = str(Path(args.diff_ida_weight))

    main_path = config_dir / "Diff_Retinex_val.json"
    rda_path = config_dir / "Diff_RDA_data_val.json"
    ida_path = config_dir / "Diff_IDA_data_val.json"

    write_json(main_path, main_cfg)
    write_json(rda_path, rda_cfg)
    write_json(ida_path, ida_cfg)

    cmd = [
        args.python_bin,
        "test_from_dataset.py",
        "--config",
        str(main_path),
        "--config_RDA",
        str(rda_path),
        "--config_IDA",
        str(ida_path),
    ]
    if args.use_gtmeans:
        cmd.extend(["--use_gtmeans", "True"])

    code = run_command(cmd, repo_root, run_dir / "run.log", status_path)
    metadata = {
        "method": "diff-retinex",
        "dataset_name": args.dataset_name,
        "pred_dir": str(pred_dir),
        "gt_dir": args.gt_dir,
        "status_path": str(status_path),
        "use_gtmeans": args.use_gtmeans,
    }
    write_json(run_dir / "run_metadata.json", metadata)
    return code, metadata


def run_reti_diff(args, run_dir: Path):
    repo_root = Path(args.repo_root)
    status_path = run_dir / "status.json"
    config_dir = ensure_dir(run_dir / "generated_configs")
    if not args.reti_template or not args.reti_weight or not args.reti_decom_weight:
        raise ValueError("reti-diff requires --reti-template, --reti-weight and --reti-decom-weight")

    with open(args.reti_template, "r", encoding="utf-8") as f:
        opt = yaml.safe_load(f)

    opt["name"] = f"RetiDiff_{args.dataset_name}"
    dataset_key = next(iter(opt["datasets"].keys()))
    opt["datasets"][dataset_key]["dataroot_gt"] = args.gt_dir
    opt["datasets"][dataset_key]["dataroot_lq"] = args.lq_dir
    opt["path"]["pretrain_network_g"] = str(Path(args.reti_weight))
    opt["pretrain_decomnet_low"] = str(Path(args.reti_decom_weight))
    opt["num_gpu"] = 1
    opt["manual_seed"] = 0

    generated_opt = config_dir / Path(args.reti_template).name
    with generated_opt.open("w", encoding="utf-8") as f:
        yaml.safe_dump(opt, f, sort_keys=False, allow_unicode=True)

    cmd = [args.python_bin, "Reti-Diff/test.py", "-opt", str(generated_opt)]
    code = run_command(cmd, repo_root, run_dir / "run.log", status_path)

    pred_dir = repo_root / "results" / opt["name"] / "visualization" / "Testset"
    if not pred_dir.exists():
        visualization_root = repo_root / "results" / opt["name"] / "visualization"
        nested_pngs = list(visualization_root.rglob("*.png"))
        if nested_pngs:
            pred_dir = nested_pngs[0].parent

    metadata = {
        "method": "reti-diff",
        "dataset_name": args.dataset_name,
        "pred_dir": str(pred_dir),
        "gt_dir": args.gt_dir,
        "status_path": str(status_path),
        "generated_opt": str(generated_opt),
    }
    write_json(run_dir / "run_metadata.json", metadata)
    return code, metadata


def main():
    args = parse_args()
    run_dir = make_run_dir(Path(args.output_root), args.method, args.dataset_name, args.run_name)
    ensure_dir(run_dir)
    update_status(run_dir / "status.json", state="created", created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    if args.method == "uretinex":
        code, metadata = run_uretinex(args, run_dir)
    elif args.method == "diff-retinex":
        code, metadata = run_diff_retinex(args, run_dir)
    elif args.method == "reti-diff":
        code, metadata = run_reti_diff(args, run_dir)
    else:
        raise ValueError(f"Unsupported method: {args.method}")

    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    if code != 0:
        raise SystemExit(code)


if __name__ == "__main__":
    main()
