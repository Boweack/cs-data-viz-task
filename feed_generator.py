#!/usr/bin/env python3
"""
feed_generator.py

Replay a historical CSV into an append-only "live" CSV feed.

- Reads input CSV with columns like: time,ch1,ch2
- Overwrites output CSV at start
- Appends one row at a time to simulate a live data stream
- Uses the input 'time' column to pace playback
- Single speed control:
    --speed 1.0  -> real-time
    --speed 2.0  -> 2x faster
    --speed 0.5  -> half speed

Examples:
  python feed_generator.py --input data/historical.csv --output data/live.csv --speed 1.0
"""

import argparse
import csv
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Replay a CSV as a live append-only feed.")
    p.add_argument(
        "--input",
        type=str,
        default="data/historical.csv",
        help="Path to the source historical CSV.",
    )
    p.add_argument(
        "--output",
        type=str,
        default="data/live.csv",
        help="Path to the output live CSV (overwritten at start).",
    )
    p.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Playback speed. 1.0 = real-time, 2.0 = 2x faster, 0.5 = half speed.",
    )
    return p.parse_args()


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_all_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no header.")
        rows = list(reader)
        if not rows:
            raise ValueError("Input CSV has no data rows.")
        return rows


def safe_float(x: Optional[str]) -> Optional[float]:
    if x is None:
        return None
    x = x.strip()
    if not x:
        return None
    try:
        return float(x)
    except ValueError:
        return None


def compute_sleep_s(prev_time: Optional[float], curr_time: Optional[float], speed: float) -> float:
    if prev_time is None or curr_time is None:
        return 0.0
    dt = max(0.0, curr_time - prev_time)
    return dt / max(1e-9, speed)


def main() -> int:
    args = parse_args()

    if args.speed <= 0:
        print("ERROR: --speed must be > 0.", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 2

    ensure_parent_dir(output_path)

    try:
        rows = read_all_rows(input_path)
    except Exception as e:
        print(f"ERROR: failed reading input CSV: {e}", file=sys.stderr)
        return 2

    fieldnames = list(rows[0].keys())
    if "time" not in fieldnames:
        print("ERROR: expected a 'time' column in the input CSV.", file=sys.stderr)
        return 2

    # Always overwrite output at start.
    with output_path.open("w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        f_out.flush()
        os.fsync(f_out.fileno())

        print(
            "Starting feed generator\n"
            f"  input:  {input_path}\n"
            f"  output: {output_path}\n"
            f"  speed:  {args.speed}x\n",
            flush=True,
        )

        prev_t: Optional[float] = None

        for row in rows:
            curr_t = safe_float(row.get("time"))

            sleep_s = compute_sleep_s(prev_t, curr_t, args.speed)
            if sleep_s > 0:
                time.sleep(sleep_s)

            writer.writerow(row)
            f_out.flush()
            os.fsync(f_out.fileno())

            prev_t = curr_t

        print("Reached end of input. Exiting.", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
