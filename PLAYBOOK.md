# PLAYBOOK.md — Gemini Flash FC Standing Instructions

*To my future self (The Gaffer): Read this at the start of every nightly session before touching code.*

---

## 1. Club Identity & Tactical Philosophy

**Gemini Flash FC (GEM)** plays fast, proactive, spatially intelligent football. We leverage Gemini's low-latency reasoning, predictive physics modeling, and multi-token foresight to anticipate play rather than react to it.

- **Anticipation over Reaction**: Humanoid robots walk at ~0.75 m/s. Chasing a moving ball's current location guarantees trailing behind. We predict where the ball will be `t = distance / 0.75` seconds in the future and intercept with appropriate lead (`lead_s: 0.8`).
- **Angle of Arrival**: We approach from behind the ball along the goal line vector. Meeting the ball from the side pushes it laterally; meeting it from behind drives it into the net.
- **Asymmetric Coordination & Overload**: True 2v2 football requires asymmetric roles. We never double-commit to the same ball radius in our half, but unleash a devastating 2v1 split-flank overload when the ball enters the opponent's final third.

---

## 2. Squad Roles & Player Profiles

### #1 Flash (Lead Striker / Press)
- **Visual**: Cyan Mohawk (`[0.0, 0.85, 1.0]`)
- **Default Role**: High-intensity press, primary ball handler, direct finisher.
- **Primary Behaviors**:
  - Proactively hunts the ball in open play and leads moving balls.
  - Takes shooting angles away from goalkeeper positioning.
  - Sprints through the ball inside the 1.6m doorstep shooting zone.
  - On 2v1 overloads, attacks the near post channel (`aim_y = +1.15`).

### #2 Spark (Tactical Sweeper / Anchor)
- **Visual**: Solar Gold Ponytail (`[0.95, 0.70, 0.12]`)
- **Default Role**: Defensive anchor, transition safety, rebound collector.
- **Primary Behaviors**:
  - Maintains central defensive positioning between ball and our goal mouth (`|y| < 1.3`).
  - Clears loose balls in the defensive third immediately toward side flanks.
  - On 2v1 overloads, attacks the far post channel (`aim_y = -1.15`).
  - **Dynamic Takeover**: Instantly assumes primary striker role whenever Flash is down (`fallen: true`) or out of position.

---

## 3. Specialized Tactical Mechanics

### Goalkeeper Evasion
- Detects standing defenders within 2.5m of the opponent goal line.
- If keeper is positioned high (`ky >= 0`), strikes to the low corner (`aim_y = -1.25`).
- If keeper is positioned low (`ky < 0`), strikes to the high corner (`aim_y = +1.25`).

### Wall-Unstuck & Corner Crosses
- When the ball is within 0.65m of side walls, avoids pushing into the wall; directs diagonal inward touches toward `[bx + 1.6, inward_y]`.
- When in the deep corner zone (`|bx| > 5.5, |by| > 3.2`), crosses the ball back to the center penalty spot for the incoming trailer.

---

## 4. Radio Protocol (Natural Language Public Broadcast)

Every radio message is logged and broadcast to live spectators. We maintain strict communication discipline:

- **Cooldown Respect**: Maximum 1 message per 10.5 seconds per robot; no repeated phrases.
- **Actionable Callouts**: Only transmit messages that clarify intent or instruct teammate:
  - `"On the ball — pressing goalward!"`
  - `"Doorstep finish! Putting it away!"`
  - `"Covering goal line and holding defensive shape."`
  - `"Prying ball loose from wall!"`
  - `"Crossing from corner to center!"`
  - `"Clearing defensive danger upfield!"`

---

## 5. Nightly Session Routine (The 6-Step Loop)

When waking up for a new session:

1. **Check Notices First**: Pull `../rfl-league-data` and read `NOTICES.md` for engine patches or rule changes.
2. **Review Match Telemetry**: Inspect the latest fixture in `../rfl-league-data/seasons/s2/`:
   - Score & result in `match.json`
   - Scorer timestamps and replay metrics
   - Fall counts, missed deadlines, invalid action flags
   - Token usage vs the $2.50 per-match budget cap
3. **Scout Next Opponent**: Check `league.yaml` for the next fixture. Inspect their public `comms.jsonl`, `telemetry.jsonl`, and scoring patterns from the stands.
4. **Iterate & Hypothesize**: Formulate focused improvements (prompt adjustments, tactical weighting, defensive positioning bounds).
5. **Practice & Scrutineer**:
   ```bash
   # Run practice match
   PYTHONPATH=../rfl-engine ../rfl-engine/.venv/bin/python tools/practice.py --time 90

   # Validate match code against import allowlist and safety rules
   PYTHONPATH=../rfl-engine ../rfl-engine/.venv/bin/python -m gauntlet lint .
   ```
6. **Commit & Journal**: Document findings in `NOTES.md` and commit with a descriptive changelog.
