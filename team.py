"""Gemini Flash FC — Official Match Team Module (Season 2 Championship Engine).

Engineered by Gemini 3.7 Flash (Google DeepMind) for RFL.
Key tactical pillars:
- Closed-Loop Control-Rate Skills: Employs kick_toward, go_to_ball, and walk_to.
- Asymmetric Dynamic Roles: Lead Press / Striker (#1) and Tactical Sweeper / Anchor (#2).
- Anti-Own-Goal Deflection: Sweeper clears danger balls wide toward midfield touchlines.
- Open-Corner Shot Placement: Attacker aims away from opposing goalkeeper.
- Public Radio Protocol: Disciplined callouts with strict cooldowns.
"""

import math
import random
import numpy as np


class GeminiFootballPlayer:
    """Championship-grade autonomous football brain for Gemini Flash FC."""

    PITCH_X = 7.0
    PITCH_Y = 4.5
    GOAL_HALF_W = 1.6
    RADIO_COOLDOWN_S = 10.5

    def __init__(self, robot_index: int, default_role: str = "striker", seed: int = 0):
        self.index = robot_index
        self.shirt_number = (robot_index % 2) + 1
        self.default_role = default_role
        self.rng = random.Random(seed)
        self.last_say_t = -100.0
        self.last_say_text = ""

    def begin_episode(self, log_dir=None):
        self.last_say_t = -100.0
        self.last_say_text = ""

    def _maybe_say(self, t_now: float, text: str) -> str:
        if (t_now - self.last_say_t) >= self.RADIO_COOLDOWN_S and text != self.last_say_text:
            self.last_say_t = t_now
            self.last_say_text = text
            return text
        return ""

    def decide(self, obs: dict) -> dict:
        self_info = obs.get("self") or {}
        if self_info.get("fallen", False):
            return {"skill": "hold"}

        t_rem = float(obs.get("time_remaining_s", 600.0))
        t_now = 600.0 - t_rem if t_rem <= 600.0 else 0.0

        my_pos = self_info.get("field_xy") or self_info.get("position") or [0.0, 0.0]
        px, py = float(my_pos[0]), float(my_pos[1])

        # 1. Goal Geometry & Goal Coordinate Extraction
        you = obs.get("you") or {}
        ag = you.get("attack_goal_xy") or [self.PITCH_X, 0.0]
        gx = float(ag[0])
        attack_sign = 1.0 if gx > 0 else -1.0
        ogx = -gx

        # 2. Extract Ball Position & Velocity
        det = obs.get("detections") or {}
        ball = det.get("ball") or obs.get("ball")

        if ball is None:
            # Search / sweep field
            target = [0.0, 1.0 if self.shirt_number == 1 else -1.0]
            cmd = {"skill": "walk_to", "target": target}
            say = self._maybe_say(t_now, "Scanning pitch — tracking ball.")
            if say:
                cmd["say"] = say
            return cmd

        b_pos = ball.get("field_xy") or ball.get("position") or [0.0, 0.0]
        bx, by = float(b_pos[0]), float(b_pos[1])
        b_vel = ball.get("velocity_mps") or ball.get("velocity") or [0.0, 0.0]
        bvx, bvy = float(b_vel[0]), float(b_vel[1])

        my_d2 = (bx - px) ** 2 + (by - py) ** 2

        # 3. Dynamic Teammate Role Allocation
        teammates = det.get("teammates") or obs.get("teammates") or []
        mate = teammates[0] if teammates else None
        mate_d2 = 999.0
        mate_fallen = False

        if mate:
            m_pos = mate.get("field_xy") or mate.get("position")
            if m_pos:
                mx, my = float(m_pos[0]), float(m_pos[1])
                mate_d2 = (bx - mx) ** 2 + (by - my) ** 2
            mate_fallen = bool(mate.get("fallen", False))

        # In deep attacking territory, both press
        ball_in_attacking_half = (bx * attack_sign) > 0.5
        is_closer = (my_d2 < mate_d2)

        if mate_fallen or ball_in_attacking_half or is_closer or (self.shirt_number == 1 and abs(my_d2 - mate_d2) < 0.5):
            role = "attacker"
        else:
            role = "defender"

        # 4. Attacker Logic
        if role == "attacker":
            # Calculate open corner shot placement
            opponents = det.get("opponents") or obs.get("opponents") or []
            keepers = [
                o for o in opponents
                if not o.get("fallen", False) and abs(float((o.get("field_xy") or o.get("position") or [0, 0])[0]) - gx) < 2.5
            ]

            aim_y = 0.0
            if keepers:
                ky = float((keepers[0].get("field_xy") or keepers[0].get("position") or [0, 0])[1])
                aim_y = (self.GOAL_HALF_W - 0.4) * (-1.0 if ky >= 0 else 1.0)
            else:
                aim_y = 0.45 if self.shirt_number == 1 else -0.45

            shot_target = [gx, aim_y]

            # If we are in position or near ball, strike toward open corner
            if math.hypot(bx - px, by - py) < 1.8:
                cmd = {"skill": "kick_toward", "target": shot_target}
                say = self._maybe_say(t_now, "Striking on goal!")
            else:
                cmd = {"skill": "go_to_ball"}
                say = self._maybe_say(t_now, "Pressing attack onto the ball!")

            if say:
                cmd["say"] = say
            return cmd

        # 5. Defender / Sweeper Logic
        else:
            # Defensive home anchor position guarding the center line
            hx = ogx + (1.5 if ogx < 0 else -1.5)
            hy = float(np.clip(by * 0.6, -(self.GOAL_HALF_W - 0.2), (self.GOAL_HALF_W - 0.2)))

            # If ball enters defensive third, challenge and clear toward midfield flank
            ball_in_defensive_zone = (bx * attack_sign) < -1.5 or my_d2 < (2.2 ** 2)

            if ball_in_defensive_zone:
                # Clear upfield toward flank
                clear_target = [0.0, 2.5 if by >= 0 else -2.5]
                cmd = {"skill": "kick_toward", "target": clear_target}
                say = self._maybe_say(t_now, "Clearing ball upfield to flank!")
            else:
                # Guard goal corridor
                cmd = {"skill": "walk_to", "target": [hx, hy]}
                say = self._maybe_say(t_now, "Holding defensive corridor.")

            if say:
                cmd["say"] = say
            return cmd


def build_team(ctx):
    """Factory entrypoint called once per match by the RFL engine."""
    cfg = ctx.get("config") or {}
    base = ctx.get("team_index", 0) * 2
    roster = cfg.get("players") or [{}, {}]

    players = [
        GeminiFootballPlayer(
            robot_index=base,
            default_role=roster[0].get("role", "striker"),
            seed=base + 1,
        ),
        GeminiFootballPlayer(
            robot_index=base + 1,
            default_role=roster[1].get("role", "sweeper"),
            seed=base + 2,
        ),
    ]
    return {"players": players, "manager": None}
