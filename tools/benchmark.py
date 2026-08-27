"""Fast head-to-head benchmark for Gemini Flash FC vs ScriptedAgent (Synthetic Athletic)."""

import sys
from pathlib import Path

here = Path(__file__).resolve().parent.parent
from gauntlet.football import run_match, FootballScriptedAgent
from gauntlet.rfl import load_team


def test_match(as_team_a=True, match_time_s=45.0):
    team_gem = load_team(here)
    
    if as_team_a:
        ctx_a = {"engine_version": "rfl-0.3", "team_index": 0, "config": {"players": [{}, {}]}}
        agents_a = team_gem.build(ctx_a)["players"]
        agents_b = [FootballScriptedAgent(2), FootballScriptedAgent(3)]
        t_names = ("Gemini Flash FC", "Synthetic Athletic")
        t_codes = ("GEM", "SYA")
        t_colors = ((0.12, 0.42, 0.92, 1.0), (0.95, 0.3, 0.15, 1.0))
        t_cnames = ("electric blue", "red")
    else:
        agents_a = [FootballScriptedAgent(0), FootballScriptedAgent(1)]
        ctx_b = {"engine_version": "rfl-0.3", "team_index": 1, "config": {"players": [{}, {}]}}
        agents_b = team_gem.build(ctx_b)["players"]
        t_names = ("Synthetic Athletic", "Gemini Flash FC")
        t_codes = ("SYA", "GEM")
        t_colors = ((0.95, 0.3, 0.15, 1.0), (0.12, 0.42, 0.92, 1.0))
        t_cnames = ("red", "electric blue")

    agents = agents_a + agents_b

    res = run_match(
        agents, match_time_s=match_time_s, mode="paused", halves=1,
        obs_mode="sdk",
        team_colors=t_colors,
        team_color_names=t_cnames,
        team_names=t_names,
        team_codes=t_codes,
        hair={0: [pl.get("hair") or {} for pl in team_gem.players], 1: {}},
        player_names={0: ["Flash", "Spark"] if as_team_a else ["Griezmatronn", "Robodinho"],
                      1: ["Griezmatronn", "Robodinho"] if as_team_a else ["Flash", "Spark"]}
    )

    side = "HOME (Team A)" if as_team_a else "AWAY (Team B)"
    gem_score = res.score[0] if as_team_a else res.score[1]
    opp_score = res.score[1] if as_team_a else res.score[0]
    print(f"\n================ {side} ({match_time_s}s) ================")
    print(f"Final Score: GEM {gem_score} - {opp_score} SYA")
    print(f"Winner: {res.winner}")
    print(f"Goals: {len(res.goals)}")
    for g in res.goals:
        print(f"  Goal at t={g['t']:.1f}s by Team {g['team']} (Robot {g['scorer']})")
    print(f"===========================================================\n")
    return gem_score, opp_score


if __name__ == "__main__":
    t = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
    print("Testing HOME match...")
    test_match(as_team_a=True, match_time_s=t)
    print("Testing AWAY match...")
    test_match(as_team_a=False, match_time_s=t)
