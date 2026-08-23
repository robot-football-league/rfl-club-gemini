"""Benchmark Gemini Flash FC against the frozen founding clubs (ScriptedAgent)."""

import sys
from pathlib import Path

here = Path(__file__).resolve().parent.parent
from gauntlet.football import run_match, FootballScriptedAgent
from gauntlet.rfl import load_team


def benchmark(match_time_s=60.0):
    team_a = load_team(here)
    # Build Gemini team (Team A, attacks +x)
    ctx_a = {"engine_version": "rfl-0.1", "team_index": 0,
             "config": {"players": [{}, {}]}}
    squad_a = team_a.build(ctx_a)
    agents_a = squad_a["players"]

    # Build Scripted team (Team B, attacks -x)
    agents_b = [FootballScriptedAgent(2), FootballScriptedAgent(3)]

    agents = agents_a + agents_b

    res = run_match(
        agents, match_time_s=match_time_s, mode="paused", halves=1,
        obs_mode="sdk",
        team_colors=((0.12, 0.42, 0.92, 1.0), (0.95, 0.3, 0.15, 1.0)),
        team_color_names=("electric blue", "red"),
        team_names=("Gemini Flash FC", "Real Machina (Scripted)"),
        team_codes=("GEM", "RMA"),
        hair={0: [pl.get("hair") or {} for pl in team_a.players], 1: {}},
        player_names={0: ["Flash", "Spark"], 1: ["CR-7000", "Zidroid"]}
    )

    print(f"\n================ BENCHMARK RESULT ================")
    print(f"Final Score: GEM {res.score[0]} - {res.score[1]} RMA")
    print(f"Winner: {res.winner}")
    print(f"Goals: {len(res.goals)}")
    for g in res.goals:
        print(f"  Goal at t={g['t']:.1f}s by Team {g['team']} (Robot {g['scorer']})")
    print(f"==================================================\n")
    return res


if __name__ == "__main__":
    t = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0
    benchmark(t)
