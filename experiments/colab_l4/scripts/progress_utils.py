import json
import os
import re
import selectors
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, Optional


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: Dict) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_json_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(^|\s)//.*?$", "", text, flags=re.M)
    return text


def read_json_with_comments(path: Path) -> Dict:
    return json.loads(strip_json_comments(path.read_text(encoding="utf-8")))


def symlink_or_copy(src: Path, dst: Path) -> None:
    ensure_dir(dst.parent)
    if dst.exists() or dst.is_symlink():
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    try:
        os.symlink(src, dst)
    except OSError:
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def gpu_snapshot() -> Dict:
    cmd = [
        "nvidia-smi",
        "--query-gpu=name,memory.total,memory.used,utilization.gpu",
        "--format=csv,noheader,nounits",
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        line = result.stdout.strip().splitlines()[0]
        name, total, used, util = [part.strip() for part in line.split(",")]
        return {
            "gpu_name": name,
            "memory_total_mb": int(total),
            "memory_used_mb": int(used),
            "utilization_gpu_pct": int(util),
        }
    except Exception:
        return {}


def update_status(status_path: Path, **fields) -> None:
    payload = {}
    if status_path.exists():
        payload = read_json(status_path)
    payload.update(fields)
    write_json(status_path, payload)


def run_command(
    cmd: Iterable[str],
    cwd: Path,
    log_path: Path,
    status_path: Path,
    env: Optional[Dict[str, str]] = None,
    heartbeat_sec: int = 30,
) -> int:
    cmd = [str(part) for part in cmd]
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    ensure_dir(log_path.parent)
    started_at = time.time()
    update_status(
        status_path,
        state="running",
        started_at=utc_now(),
        cwd=str(cwd),
        command=cmd,
        heartbeat_sec=heartbeat_sec,
        **gpu_snapshot(),
    )

    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{utc_now()}] START {' '.join(cmd)}\n")
        log_file.flush()

        process = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            env=full_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        last_heartbeat = 0.0
        last_line = ""

        while True:
            events = selector.select(timeout=1.0)
            for key, _ in events:
                line = key.fileobj.readline()
                if not line:
                    continue
                last_line = line.rstrip()
                sys.stdout.write(line)
                log_file.write(line)
                log_file.flush()

            now = time.time()
            if now - last_heartbeat >= heartbeat_sec:
                update_status(
                    status_path,
                    state="running",
                    updated_at=utc_now(),
                    elapsed_sec=round(now - started_at, 2),
                    last_line=last_line,
                    **gpu_snapshot(),
                )
                last_heartbeat = now

            if process.poll() is not None:
                for remainder in process.stdout.readlines():
                    last_line = remainder.rstrip()
                    sys.stdout.write(remainder)
                    log_file.write(remainder)
                break

        return_code = process.wait()
        finished_at = time.time()
        update_status(
            status_path,
            state="completed" if return_code == 0 else "failed",
            finished_at=utc_now(),
            elapsed_sec=round(finished_at - started_at, 2),
            return_code=return_code,
            last_line=last_line,
            **gpu_snapshot(),
        )
        log_file.write(f"[{utc_now()}] END return_code={return_code}\n")
        log_file.flush()

    return return_code
