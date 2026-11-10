"""
SupeRR Selector Season 2 - Stage 4: Player Performance Engine
Calculates:
1. Batting Performance Metrics across Normal vs. High-Pressure regimes:
   - Strike Rate (SR): 25%
   - Boundary % (4s + 6s): 25% (calibrated: boundary > strike rotation)
   - Batting Average: 20%
   - Strike Rotation Rate (1s, 2s, 3s): 18%
   - Dot Ball Avoidance Rate: 12%
   - Quality-weighted by opposition bowling strength.
2. Bowling Performance Metrics across Normal vs. High-Pressure regimes:
   - Inverted Economy Rate: 25%
   - Boundary Suppression: 25%
   - Wicket Strike Rate: 20%
   - Post-Boundary Composure: 18% (dots/wkts immediately after 4/6)
   - Dot Ball %: 12%
   - Quality-weighted by opposition batting strength.
3. Anchored Normalization & Smooth PPR (Pressure Performance Ratio).
4. Sample-size Reliability Weighting (rewards proven sample volume over flukes).
5. Exports: batter_performance.csv and bowler_performance.csv
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
PARQUET_PATH = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")
BATTER_OUT_CSV = os.path.join(DATA_DIR, "batter_performance.csv")
BOWLER_OUT_CSV = os.path.join(DATA_DIR, "bowler_performance.csv")

print("--- Stage 4: Executing Player Performance Engine ---")
df = pd.read_parquet(PARQUET_PATH)

# ============================================================
# 1. BATTING PERFORMANCE ENGINE
# ============================================================
print("\n1. Processing Batting Performance...")

# Guardrails: Min 75 balls in normal, Min 40 balls in high-pressure
bat_totals = df.groupby("striker_id").agg(
    total_balls=("is_batter_ball_faced", "sum"),
    norm_balls=("is_high_pressure_batter", lambda x: (~x & df.loc[x.index, "is_batter_ball_faced"]).sum()),
    hp_balls=("is_high_pressure_batter", lambda x: (x & df.loc[x.index, "is_batter_ball_faced"]).sum())
).reset_index()

qual_bat_ids = set(bat_totals[(bat_totals["norm_balls"] >= 75) & (bat_totals["hp_balls"] >= 40)]["striker_id"])
print(f"Qualified Batters Meeting Guardrails: {len(qual_bat_ids)}")

bat_records = []
for p_id in qual_bat_ids:
    p_df = df[df["striker_id"] == p_id]
    p_name = p_df["striker_name"].iloc[0]
    
    norm = p_df[~p_df["is_high_pressure_batter"] & p_df["is_batter_ball_faced"]]
    hp = p_df[p_df["is_high_pressure_batter"] & p_df["is_batter_ball_faced"]]
    
    # Normal Stats
    n_balls = len(norm)
    n_runs = norm["runs"].sum()
    n_outs = max(1, norm["is_wicket"].sum())
    n_bdry = norm["is_boundary"].sum()
    n_rot = norm["is_strike_rotation"].sum()
    n_dots = norm["is_dot_ball"].sum()
    n_opp = norm["opp_bowling_team_quality"].mean()
    
    # High-Pressure Stats
    hp_balls = len(hp)
    hp_runs = hp["runs"].sum()
    hp_outs = max(1, hp["is_wicket"].sum())
    hp_bdry = hp["is_boundary"].sum()
    hp_rot = hp["is_strike_rotation"].sum()
    hp_dots = hp["is_dot_ball"].sum()
    hp_opp = hp["opp_bowling_team_quality"].mean()
    
    bat_records.append({
        "player_id": p_id,
        "player_name": p_name,
        "total_balls": n_balls + hp_balls,
        "norm_balls": n_balls,
        "norm_runs": n_runs,
        "norm_sr": (n_runs / n_balls) * 100,
        "norm_avg": n_runs / n_outs,
        "norm_bdry_pct": (n_bdry / n_balls) * 100,
        "norm_rot_pct": (n_rot / n_balls) * 100,
        "norm_dot_avoid": (1.0 - (n_dots / n_balls)) * 100,
        "norm_opp_quality": n_opp,
        "hp_balls": hp_balls,
        "hp_runs": hp_runs,
        "hp_sr": (hp_runs / hp_balls) * 100,
        "hp_avg": hp_runs / hp_outs,
        "hp_bdry_pct": (hp_bdry / hp_balls) * 100,
        "hp_rot_pct": (hp_rot / hp_balls) * 100,
        "hp_dot_avoid": (1.0 - (hp_dots / hp_balls)) * 100,
        "hp_opp_quality": hp_opp
    })

bdf = pd.DataFrame(bat_records)

def anchor_scale(val, low, high):
    return np.clip((val - low) / (high - low), 0.05, 1.0) * 100

# Batting Normal Score (Weighted: Boundary 25%, SR 25%, Avg 20%, Rotation 18%, Dot Avoid 12%)
bdf["norm_score"] = (
    0.25 * anchor_scale(bdf["norm_bdry_pct"], 5.0, 28.0) +
    0.25 * anchor_scale(bdf["norm_sr"], 90.0, 180.0) +
    0.20 * anchor_scale(bdf["norm_avg"], 12.0, 45.0) +
    0.18 * anchor_scale(bdf["norm_rot_pct"], 30.0, 55.0) +
    0.12 * anchor_scale(bdf["norm_dot_avoid"], 45.0, 75.0)
) * (bdf["norm_opp_quality"] / 0.80)

# Batting High-Pressure Score
bdf["hp_score"] = (
    0.25 * anchor_scale(bdf["hp_bdry_pct"], 5.0, 28.0) +
    0.25 * anchor_scale(bdf["hp_sr"], 90.0, 180.0) +
    0.20 * anchor_scale(bdf["hp_avg"], 12.0, 45.0) +
    0.18 * anchor_scale(bdf["hp_rot_pct"], 30.0, 55.0) +
    0.12 * anchor_scale(bdf["hp_dot_avoid"], 45.0, 75.0)
) * (bdf["hp_opp_quality"] / 0.80)

# Pressure Performance Ratio (PPR)
bdf["ppr"] = np.clip(bdf["hp_score"] / np.maximum(20.0, bdf["norm_score"]), 0.60, 1.60)

# Sample Size Reliability Weight (sqrt scaling up to 150 HP balls)
bdf["reliability"] = np.sqrt(np.clip(bdf["hp_balls"] / 150.0, 0.25, 1.0))

# Composite Final Rank Score
bdf["final_rank_score"] = (0.75 * bdf["hp_score"] + 0.25 * (bdf["ppr"] * 50.0)) * bdf["reliability"]

bdf.sort_values(by="final_rank_score", ascending=False, inplace=True)
bdf["rank"] = range(1, len(bdf) + 1)
bdf.to_csv(BATTER_OUT_CSV, index=False)
print(f"Saved Batting Performance to {BATTER_OUT_CSV}")

# ============================================================
# 2. BOWLING PERFORMANCE ENGINE
# ============================================================
print("\n2. Processing Bowling Performance...")

# Guardrails: Min 75 balls in normal, Min 40 balls in high-pressure
bowl_totals = df.groupby("bowler_id").agg(
    total_balls=("is_legal_bowler_ball", "sum"),
    norm_balls=("is_high_pressure_bowler", lambda x: (~x & df.loc[x.index, "is_legal_bowler_ball"]).sum()),
    hp_balls=("is_high_pressure_bowler", lambda x: (x & df.loc[x.index, "is_legal_bowler_ball"]).sum())
).reset_index()

qual_bowl_ids = set(bowl_totals[(bowl_totals["norm_balls"] >= 75) & (bowl_totals["hp_balls"] >= 40)]["bowler_id"])
print(f"Qualified Bowlers Meeting Guardrails: {len(qual_bowl_ids)}")

bowl_records = []
for p_id in qual_bowl_ids:
    p_df = df[df["bowler_id"] == p_id]
    p_name = p_df["bowler_name"].iloc[0]
    
    norm = p_df[~p_df["is_high_pressure_bowler"] & p_df["is_legal_bowler_ball"]]
    hp = p_df[p_df["is_high_pressure_bowler"] & p_df["is_legal_bowler_ball"]]
    
    # Normal Stats
    n_balls = len(norm)
    n_runs = norm["bowler_runs_conceded"].sum()
    n_wkts = max(1, norm["is_bowler_wicket"].sum())
    n_dots = norm["is_dot_ball"].sum()
    n_bdry = norm["is_boundary"].sum()
    n_opp = norm["opp_batting_team_quality"].mean()
    
    # High-Pressure Stats
    hp_balls = len(hp)
    hp_runs = hp["bowler_runs_conceded"].sum()
    hp_wkts = max(1, hp["is_bowler_wicket"].sum())
    hp_dots = hp["is_dot_ball"].sum()
    hp_bdry = hp["is_boundary"].sum()
    hp_opp = hp["opp_batting_team_quality"].mean()
    
    # Post-boundary Composure (HP)
    hp_post_b = hp[hp["bowler_post_boundary"]]
    hp_post_b_count = len(hp_post_b)
    hp_post_b_good = (hp_post_b["is_dot_ball"] | hp_post_b["is_bowler_wicket"]).sum() if hp_post_b_count > 0 else 0
    hp_post_b_comp = (hp_post_b_good / max(1, hp_post_b_count)) * 100
    
    # Post-boundary Composure (Normal)
    norm_post_b = norm[norm["bowler_post_boundary"]]
    norm_post_b_count = len(norm_post_b)
    norm_post_b_good = (norm_post_b["is_dot_ball"] | norm_post_b["is_bowler_wicket"]).sum() if norm_post_b_count > 0 else 0
    norm_post_b_comp = (norm_post_b_good / max(1, norm_post_b_count)) * 100
    
    bowl_records.append({
        "player_id": p_id,
        "player_name": p_name,
        "total_balls": n_balls + hp_balls,
        "norm_balls": n_balls,
        "norm_runs": n_runs,
        "norm_econ": (n_runs / n_balls) * 6.0,
        "norm_wsr": n_balls / n_wkts,
        "norm_dot_pct": (n_dots / n_balls) * 100,
        "norm_bdry_pct": (n_bdry / n_balls) * 100,
        "norm_post_b_comp": norm_post_b_comp,
        "norm_opp_quality": n_opp,
        "hp_balls": hp_balls,
        "hp_runs": hp_runs,
        "hp_wkts": hp_wkts,
        "hp_econ": (hp_runs / hp_balls) * 6.0,
        "hp_wsr": hp_balls / hp_wkts,
        "hp_dot_pct": (hp_dots / hp_balls) * 100,
        "hp_bdry_pct": (hp_bdry / hp_balls) * 100,
        "hp_post_b_comp": hp_post_b_comp,
        "hp_opp_quality": hp_opp
    })

bwdf = pd.DataFrame(bowl_records)

def invert_scale(val, best, worst):
    return np.clip((worst - val) / (worst - best), 0.05, 1.0) * 100

# Bowling Normal Score (Inverted Econ 25%, Boundary Suppression 25%, WSR 20%, Post-Boundary 18%, Dot% 12%)
bwdf["norm_score"] = (
    0.25 * invert_scale(bwdf["norm_econ"], 6.0, 11.5) +
    0.25 * invert_scale(bwdf["norm_bdry_pct"], 8.0, 26.0) +
    0.20 * invert_scale(bwdf["norm_wsr"], 12.0, 36.0) +
    0.18 * anchor_scale(bwdf["norm_post_b_comp"], 20.0, 55.0) +
    0.12 * anchor_scale(bwdf["norm_dot_pct"], 25.0, 50.0)
) * (bwdf["norm_opp_quality"] / 0.80)

# Bowling High-Pressure Score
bwdf["hp_score"] = (
    0.25 * invert_scale(bwdf["hp_econ"], 6.0, 11.5) +
    0.25 * invert_scale(bwdf["hp_bdry_pct"], 8.0, 26.0) +
    0.20 * invert_scale(bwdf["hp_wsr"], 12.0, 36.0) +
    0.18 * anchor_scale(bwdf["hp_post_b_comp"], 20.0, 55.0) +
    0.12 * anchor_scale(bwdf["hp_dot_pct"], 25.0, 50.0)
) * (bwdf["hp_opp_quality"] / 0.80)

# Pressure Performance Ratio (PPR)
bwdf["ppr"] = np.clip(bwdf["hp_score"] / np.maximum(20.0, bwdf["norm_score"]), 0.60, 1.60)

# Sample Size Reliability Weight
bwdf["reliability"] = np.sqrt(np.clip(bwdf["hp_balls"] / 150.0, 0.25, 1.0))

# Composite Final Rank Score
bwdf["final_rank_score"] = (0.75 * bwdf["hp_score"] + 0.25 * (bwdf["ppr"] * 50.0)) * bwdf["reliability"]

bwdf.sort_values(by="final_rank_score", ascending=False, inplace=True)
bwdf["rank"] = range(1, len(bwdf) + 1)
bwdf.to_csv(BOWLER_OUT_CSV, index=False)
print(f"Saved Bowling Performance to {BOWLER_OUT_CSV}")

print("\n=== Stage 4 Preview: Top 10 Batters ===")
print(bdf[["rank", "player_name", "hp_balls", "hp_runs", "hp_sr", "hp_avg", "hp_bdry_pct", "ppr", "final_rank_score"]].head(10).to_string(index=False))

print("\n=== Stage 4 Preview: Top 10 Bowlers ===")
print(bwdf[["rank", "player_name", "hp_balls", "hp_econ", "hp_wsr", "hp_post_b_comp", "ppr", "final_rank_score"]].head(10).to_string(index=False))
print("\nStage 4 completed successfully!")
