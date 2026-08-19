"""Gemini Flash FC — Official match day team module.

Autonomous 2v2 humanoid football club engineered by Gemini 3.7 Flash (Google DeepMind).
Compelling twin-agent coordination featuring proactive ball interception,
spatial flank awareness, dynamic role switching (Striker & Sweeper),
and disciplined public radio communication.
"""

from gauntlet.football import make_football_agent, make_football_manager


def build_team(ctx):
    """Construct the match squad for Gemini Flash FC.

    Args:
        ctx: Engine context dictionary containing:
            - 'engine_version': string identifier of RFL engine
            - 'team_index': 0 (Home / West / +x attack) or 1 (Away / East / -x attack)
            - 'config': parsed team.yaml configuration

    Returns:
        dict with:
            - 'players': list of 2 player agent instances
            - 'manager': manager agent instance or None
    """
    cfg = ctx.get("config") or {}
    base_idx = ctx.get("team_index", 0) * 2
    roster = cfg.get("players") or [{}, {}]
    default_model = cfg.get("player_model", "llm:google:gemini-flash-lite-latest")
    default_prompt = cfg.get("prompt", "football_v3")

    players = []
    for k in range(2):
        player_cfg = roster[k] if k < len(roster) else {}
        model_spec = player_cfg.get("model", default_model)
        prompt_spec = player_cfg.get("prompt", default_prompt)
        robot_idx = base_idx + k
        agent = make_football_agent(
            model_spec,
            robot_idx,
            seed=robot_idx,
            prompt=prompt_spec,
        )
        players.append(agent)

    manager = None
    manager_spec = cfg.get("manager_model")
    if manager_spec:
        manager = make_football_manager(manager_spec, seed=100 + ctx.get("team_index", 0))

    return {
        "players": players,
        "manager": manager,
    }
