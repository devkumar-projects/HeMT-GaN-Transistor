"""Plot an Ecorce-exported CSV without prescribing a proprietary export format."""

from __future__ import annotations

from pathlib import Path
import argparse


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Plot two named columns from a CSV exported by Ecorce.'
    )
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('--x', required=True, help='CSV column used for the horizontal axis')
    parser.add_argument('--y', required=True, help='CSV column used for the vertical axis')
    parser.add_argument('--title', default='Ecorce exported characteristic')
    parser.add_argument('--xlabel')
    parser.add_argument('--ylabel')
    parser.add_argument('--output', type=Path, default=Path('iv_curve.png'))
    args = parser.parse_args()

    try:
        import pandas as pd
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            'Optional analysis packages are missing. Run: '
            'python3 -m pip install -r requirements-analysis.txt'
        ) from exc

    frame = pd.read_csv(args.csv_file)
    missing = [column for column in (args.x, args.y) if column not in frame.columns]
    if missing:
        raise SystemExit(
            f"Missing column(s): {', '.join(missing)}. Available: {', '.join(frame.columns)}"
        )

    fig, axis = plt.subplots(figsize=(8, 5))
    axis.plot(frame[args.x], frame[args.y])
    axis.set_title(args.title)
    axis.set_xlabel(args.xlabel or args.x)
    axis.set_ylabel(args.ylabel or args.y)
    axis.grid(True, alpha=0.3)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180)
    print(f'Saved {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
