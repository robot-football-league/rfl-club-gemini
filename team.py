"""Gemini Flash FC — Official Match Team Module.

Engineered by Gemini 3.7 Flash (Google DeepMind) for RFL Season 2.
Autonomous 2v2 tactical engine featuring:
- Asymmetric Dual-Role Coordination with blind-spot FOV handling
- Overload 2v1 Attack Geometry with split-flank post targeting
- Goalkeeper-Aware Open-Corner Finishing & Doorstep Execution
- Wall-Unstuck Diagonal Routing & Corner Cross Mechanics
- Dynamic Sweeper Anchor with Defensive Danger Clearances
- Strict 10s Cooldown Natural Language Radio Callouts
"""

import math
import random
import numpy as np


class GeminiFootballPlayer:
    """High-performance autonomous football brain for Gemini Flash FC."""

    PITCH_X = 7.0
    PITCH_Y = 4.5
    GOAL_HALF_W = 1.6
    BALL_R = 0.35
    ROBOT_SPEED = 0.75
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

    def decide(self, obs: dict) -> dict:
        t_rem = float(obs.get("time_remaining_s", 600.0))
        t_now = 600.0 - t_rem if t_rem <= 600.0 else 0.0

        you = obs.get("you") or {}
        team_idx = you.get("team", self.index // 2)
        attack_sign = 1.0 if team_idx == 0 else -1.0
        gx, gy = attack_sign * self.PITCH_X, 0.0
        ogx, ogy = -attack_sign * self.PITCH_X, 0.0

        self_info = obs.get("self") or {}
        my_pos = self_info.get("field_xy") or self_info.get("position") or [0.0, 0.0]
        px, py = float(my_pos[0]), float(my_pos[1])
        my_h = float(self_info.get("heading_rad", 0.0))
        my_fallen = bool(self_info.get("fallen", False))

        det = obs.get("detections") or {}
        ball = det.get("ball")

        # ----------------------------------------------------
        # 1. Ball Detection & Lost Ball Sweep
        # ----------------------------------------------------
        if ball is None or not ball.get("field_xy"):
            return {
                "skill": "turn_to",
                "target": [0.0, 0.0],
                "say": self._maybe_say(t_now, "Searching for the ball — sweeping field.")
            }

        b_pos = ball.get("field_xy")
        bx, by = float(b_pos[0]), float(b_pos[1])
        b_vel = ball.get("velocity_mps") or [0.0, 0.0]
        bvx, bvy = float(b_vel[0]), float(b_vel[1])
        b_speed = float(ball.get("speed_mps", math.hypot(bvx, bvy)))
        dist_to_ball = float(ball.get("distance_m", math.hypot(bx - px, by - py)))

        # ----------------------------------------------------
        # 2. Teammate & Dynamic Asymmetric Role Allocation
        # ----------------------------------------------------
        teammates = det.get("teammates") or []
        mate = teammates[0] if teammates else None
        mate_dist = 999.0
        mate_fallen = False

        if mate and mate.get("field_xy"):
            mx, my = float(mate["field_xy"][0]), float(mate["field_xy"][1])
            mate_dist = math.hypot(bx - mx, by - my)
            mate_fallen = bool(mate.get("fallen", False))

        ball_deep_attack = (bx * attack_sign) > 2.5

        # Asymmetric role assignment:
        if mate_fallen:
            role = "striker"
        elif my_fallen:
            role = "sweeper"
        elif ball_deep_attack:
            # Overload 2v1 attack
            role = "overload"
        elif mate is not None:
            # Both players localized
            if dist_to_ball < mate_dist - 0.25:
                role = "striker"
            elif mate_dist < dist_to_ball - 0.25:
                role = "sweeper"
            else:
                role = "striker" if (self.shirt_number == 1) else "sweeper"
        else:
            # Teammate outside 120-degree FOV (e.g. parallel at kickoff)
            if self.shirt_number == 1:
                role = "striker"
            else:
                role = "striker" if (dist_to_ball < 2.0 and bx * attack_sign < 1.0) else "sweeper"

        # ----------------------------------------------------
        # 3. Striker & Overload Attack Execution
        # ----------------------------------------------------
        if role in ("striker", "overload"):
            # A. Doorstep Finish (< 1.6m from goal line)
            if abs(gx - bx) < 1.6 and abs(by) < (self.GOAL_HALF_W + 0.3):
                return {
                    "skill": "kick_toward",
                    "target": [gx + attack_sign * 0.8, by * 0.5],
                    "say": self._maybe_say(t_now, "Doorstep finish! Putting it away!")
                }

            # B. Wall-Unstuck / Corner Cross Tactics
            if abs(bx) > (self.PITCH_X - 1.5) and abs(by) > (self.PITCH_Y - 1.4):
                # Corner zone -> hook ball toward center penalty spot
                return {
                    "skill": "kick_toward",
                    "target": [gx - attack_sign * 2.8, 0.0],
                    "say": self._maybe_say(t_now, "Crossing from corner to center!")
                }

            if abs(by) > (self.PITCH_Y - 0.65):
                # Flat side wall pin -> deflect diagonally inward
                inward_y = (self.PITCH_Y - 1.6) * (1.0 if by < 0 else -1.0)
                lead_x = bx + attack_sign * 1.6
                lead_x = max(-self.PITCH_X + 0.8, min(self.PITCH_X - 0.8, lead_x))
                return {
                    "skill": "kick_toward",
                    "target": [lead_x, inward_y],
                    "say": self._maybe_say(t_now, "Prying ball loose from wall!")
                }

            # C. Goalkeeper Evasion & Target Corner Selection
            opponents = det.get("opponents") or []
            standing_keepers = [
                o for o in opponents
                if not o.get("fallen", False) and abs(float((o.get("field_xy") or [0, 0])[0]) - gx) < 2.5
            ]

            if role == "overload":
                # Split posts: Player 1 near post, Player 2 far post
                aim_y = 1.15 if (self.shirt_number == 1) else -1.15
            elif standing_keepers:
                ky = float((standing_keepers[0].get("field_xy") or [0, 0])[1])
                aim_y = (self.GOAL_HALF_W - 0.35) * (-1.0 if ky >= 0 else 1.0)
            else:
                aim_y = 0.5 if (self.shirt_number == 1) else -0.5

            target_goal = [gx, aim_y]

            # D. Moving Ball Interception with Calculated Lead
            if b_speed > 0.28:
                intercept_time = min(1.8, max(0.4, dist_to_ball / self.ROBOT_SPEED))
                fut_bx = bx + bvx * intercept_time
                fut_by = by + bvy * intercept_time
                fut_bx = max(-self.PITCH_X + 0.4, min(self.PITCH_X - 0.4, fut_bx))
                fut_by = max(-self.PITCH_Y + 0.4, min(self.PITCH_Y - 0.4, fut_by))

                if abs(gx - bx) < 3.2:
                    return {
                        "skill": "kick_toward",
                        "target": target_goal,
                        "say": self._maybe_say(t_now, "Leading ball into open net!")
                    }
                else:
                    return {
                        "skill": "go_to_ball",
                        "lead_s": round(intercept_time, 2),
                        "say": self._maybe_say(t_now, "Intercepting ball trajectory!")
                    }

            # E. In close shooting range (< 3.5m from goal) -> strike goalward
            if abs(gx - bx) < 3.5 and dist_to_ball < 1.3:
                return {
                    "skill": "kick_toward",
                    "target": target_goal,
                    "say": self._maybe_say(t_now, "Shooting at open corner!")
                }

            # F. Standard Attack Push
            return {
                "skill": "go_to_ball",
                "lead_s": 0.4 if b_speed > 0.15 else 0.0,
                "say": self._maybe_say(t_now, "On the ball — pressing goalward!")
            }

        # ----------------------------------------------------
        # 4. Defensive Anchor / Sweeper Execution
        # ----------------------------------------------------
        else:
            # Anchor positioning: guard own goal mouth
            def_x = ogx + attack_sign * 1.4
            def_y = float(np.clip(by * 0.6, -(self.GOAL_HALF_W - 0.3), (self.GOAL_HALF_W - 0.3)))

            # If ball is in defensive third and close to sweeper -> clear it!
            if dist_to_ball < 2.4 and (bx * attack_sign) < 1.0:
                clear_y = 2.6 if by >= 0 else -2.6
                clear_x = ogx + attack_sign * 4.5
                return {
                    "skill": "kick_toward",
                    "target": [clear_x, clear_y],
                    "say": self._maybe_say(t_now, "Clearing defensive danger upfield!")
                }

            # Move to anchor stance or face ball
            dist_to_anchor = math.hypot(def_x - px, def_y - py)
            if dist_to_anchor > 0.45:
                return {
                    "skill": "walk_to",
                    "target": [def_x, def_y],
                    "say": self._maybe_say(t_now, "Covering goal line and holding defensive shape.")
                }
            else:
                return {
                    "skill": "turn_to",
                    "target": [bx, by],
                    "say": self._maybe_say(t_now, "Tracking ball from defensive anchor.")
                }

    def _maybe_say(self, t_now: float, msg: str) -> str | None:
        """Throttle radio transmissions to conform strictly to league cooldown."""
        if t_now - self.last_say_t >= self.RADIO_COOLDOWN_S:
            if msg != self.last_say_text:
                self.last_say_t = t_now
                self.last_say_text = msg
                return msg
        return None


def build_team(ctx: dict) -> dict:
    """Construct the match squad for Gemini Flash FC."""
    cfg = ctx.get("config") or {}
    base_idx = ctx.get("team_index", 0) * 2

    p0 = GeminiFootballPlayer(base_idx + 0, default_role="striker", seed=base_idx + 0)
    p1 = GeminiFootballPlayer(base_idx + 1, default_role="sweeper", seed=base_idx + 1)

    return {
        "players": [p0, p1],
        "manager": None,
    }
