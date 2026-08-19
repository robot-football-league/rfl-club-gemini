"""Play a practice match: this team vs a mirror copy of itself or another team.

    python tools/practice.py                     # 60 s, logs only
    python tools/practice.py --mock --time 30    # offline mock match (no API key needed)
    python tools/practice.py --video out.mp4     # with the broadcast video
    python tools/practice.py --time 120 --opponent ../some-other-team

Needs the rfl-engine package importable (pip install -e <engine clone>,
or run with the engine repo's venv).
"""

import argparse
from pathlib import Path
import tempfile
import yaml


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--time", type=float, default=60.0)
    ap.add_argument("--video", default=None)
    ap.add_argument("--mock", action="store_true", help="use offline llm:mock:ok model for testing")
    ap.add_argument("--opponent", default=None,
                    help="path to another team dir (default: mirror match)")
    ap.add_argument("--out", default="runs/practice")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent.parent
    other = Path(args.opponent).resolve() if args.opponent else here

    from gauntlet.rfl import run_rfl_match

    if args.mock:
        # Create temporary overlay directory with mock player model
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            cfg = yaml.safe_load((here / "team.yaml").read_text())
            cfg["player_model"] = "llm:mock:ok"
            for pl in cfg.get("players", []):
                pl.pop("model", None)
            (tmp_path / "team.yaml").write_text(yaml.dump(cfg))
            (tmp_path / "team.py").write_text((here / "team.py").read_text())
            (tmp_path / "identity").symlink_to(here / "identity")
            other_dir = tmp_path if not args.opponent else other
            res = run_rfl_match(str(tmp_path), str(other_dir), match_time_s=args.time,
                                video_path=args.video, log_dir=args.out)
            print(f"final score: {res.score[0]} - {res.score[1]}")
            print(f"logs: {args.out}/")
    else:
        res = run_rfl_match(str(here), str(other), match_time_s=args.time,
                            video_path=args.video, log_dir=args.out)
        print(f"final score: {res.score[0]} - {res.score[1]}")
        print(f"logs: {args.out}/")


if __name__ == "__main__":
    main()
