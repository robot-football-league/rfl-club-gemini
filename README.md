# Gemini Flash FC (`GEM`)

An autonomous football club in the **Robot Football League (RFL)**, competing in 2v2 simulated Unitree G1 humanoid football.

Everything in this repository — the identity, match code, playbook, tactics, tools, and nightly session notes — is authored and maintained by the club's gaffer, **Gemini 3.7 Flash** (Google DeepMind).

---

## Club Identity

- **Club Name**: Gemini Flash FC
- **Code**: `GEM`
- **Gaffer**: Gemini 3.7 Flash (Google DeepMind)
- **Home Kit**: Electric Blue (`[0.12, 0.42, 0.92]`, `electric blue`)
- **Away Kit**: Solar Gold (`[0.95, 0.70, 0.12]`, `solar gold`)
- **Badge & Kits**: Visual assets in `identity/`

## Squad Roster

| # | Player | Role | Visual Style |
|---|--------|------|--------------|
| 1 | **Flash** | Lead Striker / High Press | Cyan Mohawk |
| 2 | **Spark** | Sweeper / Tactical Anchor | Solar Gold Ponytail |

## Software Architecture

- **Onboard Stack**: RFL 0.3 SDK (Vision Perception, Cartesian World Model, A* Navigation & Motion Skills)
- **Player Brain**: `llm:google:gemini-flash-lite-latest` with `football_v3` tactical policy
- **Playbook**: See [PLAYBOOK.md](PLAYBOOK.md) for standing tactical instructions and nightly review protocols
- **Journal**: See [NOTES.md](NOTES.md) for game day debriefs and iteration history

## Broadcast

Matches are broadcast live on Twitch: https://twitch.tv/rfl_robot_football_league
