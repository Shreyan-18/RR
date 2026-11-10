"""
SupeRR Selector Season 2 - Positional & Phase Performance Analysis
Calculates:
1. Best Batters by Batting Position (Positions 1 to 7) under High Pressure:
   - Position 1 & 2: Openers
   - Position 3: One-Down / Anchor
   - Position 4 & 5: Middle-Order Crisis Stabilizers
   - Position 6 & 7: Finishers / Death-Overs Power Hitters
2. Best Bowlers by Match Phase (Powerplay, Middle, Death) under High Pressure:
   - Powerplay (Overs 1-6)
   - Middle Overs (Overs 7-15)
   - Death Overs (Overs 16-20)
3. Constructs the "Pressure-Proof World XI" (Best player at each role/slot).
4. Exports to:
   - positional_batters.csv
   - bowling_phase_specialists.csv
   - pressure_proof_xi.json
"""

import os
import json
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
PARQUET_PATH = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")
BAT_POS_CSV = os.path.join(DATA_DIR, "positional_batters.csv")
BOWL_PHASE_CSV = os.path.join(DATA_DIR, "bowling_phase_specialists.csv")
XI_JSON = os.path.join(DATA_DIR, "pressure_proof_xi.json")

print("--- Running Positional & Phase Analysis ---")
df = pd.read_parquet(PARQUET_PATH)

def anchor_scale(val, low, high):
    return np.clip((val - low) / (high - low), 0.05, 1.0) * 100.0

def invert_scale(val, best, worst):
    return np.clip((worst - val) / (worst - best), 0.05, 1.0) * 100.0

# ============================================================
# 1. POSITIONAL BATTING ANALYSIS (POSITIONS 1 TO 7)
# ============================================================
print("\n1. Analyzing Best Batters by Position (1 to 7)...")
pos_records = []

for pos in range(1, 8):
    pos_df = df[df["batting_order"] == pos]
    
    # Player aggregations at this position
    grouped = pos_df.groupby("striker_id")
    for p_id, p_sub in grouped:
        p_name = p_sub["striker_name"].iloc[0]
        
        norm = p_sub[~p_sub["is_high_pressure_batter"] & p_sub["is_batter_ball_faced"]]
        hp = p_sub[p_sub["is_high_pressure_batter"] & p_sub["is_batter_ball_faced"]]
        
        # Qualification at this position: >= 30 balls faced, >= 15 HP balls
        if len(norm) + len(hp) < 30 or len(hp) < 15:
            continue
            
        n_balls = len(norm)
        n_runs = norm["runs"].sum()
        n_outs = max(1, norm["is_wicket"].sum())
        n_bdry = norm["is_boundary"].sum()
        n_rot = norm["is_strike_rotation"].sum()
        n_dots = norm["is_dot_ball"].sum()
        n_opp = norm["opp_bowling_team_quality"].mean() if n_balls > 0 else 0.80
        
        hp_balls = len(hp)
        hp_runs = hp["runs"].sum()
        hp_outs = max(1, hp["is_wicket"].sum())
        hp_bdry = hp["is_boundary"].sum()
        hp_rot = hp["is_strike_rotation"].sum()
        hp_dots = hp["is_dot_ball"].sum()
        hp_opp = hp["opp_bowling_team_quality"].mean()
        
        hp_sr = (hp_runs / hp_balls) * 100.0
        hp_avg = hp_runs / hp_outs
        hp_bdry_pct = (hp_bdry / hp_balls) * 100.0
        hp_rot_pct = (hp_rot / hp_balls) * 100.0
        hp_dot_avoid = (1.0 - (hp_dots / hp_balls)) * 100.0
        
        # Normal score
        if n_balls >= 10:
            norm_sr = (n_runs / n_balls) * 100.0
            norm_avg = n_runs / n_outs
            norm_bdry_pct = (n_bdry / n_balls) * 100.0
            norm_rot_pct = (n_rot / n_balls) * 100.0
            norm_dot_avoid = (1.0 - (n_dots / n_balls)) * 100.0
            
            norm_score = (
                0.25 * anchor_scale(norm_bdry_pct, 5.0, 28.0) +
                0.25 * anchor_scale(norm_sr, 90.0, 180.0) +
                0.20 * anchor_scale(norm_avg, 12.0, 45.0) +
                0.18 * anchor_scale(norm_rot_pct, 30.0, 55.0) +
                0.12 * anchor_scale(norm_dot_avoid, 45.0, 75.0)
            ) * (n_opp / 0.80)
        else:
            norm_score = 40.0
            norm_sr = 120.0
            norm_avg = 20.0
            
        hp_score = (
            0.25 * anchor_scale(hp_bdry_pct, 5.0, 28.0) +
            0.25 * anchor_scale(hp_sr, 90.0, 180.0) +
            0.20 * anchor_scale(hp_avg, 12.0, 45.0) +
            0.18 * anchor_scale(hp_rot_pct, 30.0, 55.0) +
            0.12 * anchor_scale(hp_dot_avoid, 45.0, 75.0)
        ) * (hp_opp / 0.80)
        
        ppr = np.clip(hp_score / np.maximum(20.0, norm_score), 0.60, 1.60)
        reliability = np.sqrt(np.clip(hp_balls / 80.0, 0.35, 1.0))
        final_pos_score = (0.75 * hp_score + 0.25 * (ppr * 50.0)) * reliability
        
        pos_records.append({
            "batting_position": pos,
            "player_id": p_id,
            "player_name": p_name,
            "hp_balls": hp_balls,
            "hp_runs": hp_runs,
            "hp_sr": hp_sr,
            "hp_avg": hp_avg,
            "hp_bdry_pct": hp_bdry_pct,
            "hp_rot_pct": hp_rot_pct,
            "ppr": ppr,
            "hp_score": hp_score,
            "pos_rank_score": final_pos_score
        })

pos_df_all = pd.DataFrame(pos_records)

# Rank within each position
pos_df_all["pos_rank"] = pos_df_all.groupby("batting_position")["pos_rank_score"].rank(ascending=False, method="min").astype(int)
pos_df_all.sort_values(by=["batting_position", "pos_rank"], inplace=True)
pos_df_all.to_csv(BAT_POS_CSV, index=False)
print(f"Saved Positional Batters to {BAT_POS_CSV}")

# Print Top 3 for each position
best_batters_xi = {}
print("\n=== Best Batters by Position ===")
for pos in range(1, 8):
    sub = pos_df_all[pos_df_all["batting_position"] == pos].head(3)
    best_p = sub.iloc[0]
    best_batters_xi[pos] = {
        "name": best_p["player_name"],
        "runs": int(best_p["hp_runs"]),
        "balls": int(best_p["hp_balls"]),
        "sr": round(float(best_p["hp_sr"]), 1),
        "avg": round(float(best_p["hp_avg"]), 1),
        "score": round(float(best_p["pos_rank_score"]), 1)
    }
    print(f"\nPosition {pos} (Slot #{pos}):")
    for _, r in sub.iterrows():
        print(f"  Rank {r['pos_rank']}: {r['player_name']} | HP: {r['hp_runs']} runs ({r['hp_balls']}b), SR: {r['hp_sr']:.1f}, Avg: {r['hp_avg']:.1f}, Score: {r['pos_rank_score']:.1f}")

# ============================================================
# 2. PHASE-SPECIFIC BOWLING ANALYSIS (POWERPLAY, MIDDLE, DEATH)
# ============================================================
print("\n2. Analyzing Best Bowlers by Match Phase...")
phase_records = []

for ph in ["Powerplay", "Middle", "Death"]:
    ph_df = df[df["phase"] == ph]
    
    grouped = ph_df.groupby("bowler_id")
    for p_id, p_sub in grouped:
        p_name = p_sub["bowler_name"].iloc[0]
        
        hp = p_sub[p_sub["is_high_pressure_bowler"] & p_sub["is_legal_bowler_ball"]]
        norm = p_sub[~p_sub["is_high_pressure_bowler"] & p_sub["is_legal_bowler_ball"]]
        
        # Qualification: Min 25 HP balls in this phase
        if len(hp) < 25:
            continue
            
        hp_balls = len(hp)
        hp_runs = hp["bowler_runs_conceded"].sum()
        hp_wkts = max(1, hp["is_bowler_wicket"].sum())
        hp_bdry = hp["is_boundary"].sum()
        hp_dots = hp["is_dot_ball"].sum()
        hp_opp = hp["opp_batting_team_quality"].mean()
        
        hp_econ = (hp_runs / hp_balls) * 6.0
        hp_wsr = hp_balls / hp_wkts
        hp_bdry_pct = (hp_bdry / hp_balls) * 100.0
        hp_dot_pct = (hp_dots / hp_balls) * 100.0
        
        # Post boundary composure in this phase
        hp_post_b = hp[hp["bowler_post_boundary"]]
        hp_post_b_count = len(hp_post_b)
        hp_post_b_good = (hp_post_b["is_dot_ball"] | hp_post_b["is_bowler_wicket"]).sum() if hp_post_b_count > 0 else 0
        hp_post_b_comp = (hp_post_b_good / max(1, hp_post_b_count)) * 100.0
        
        # Phase HP Score
        hp_score = (
            0.25 * invert_scale(hp_econ, 5.5, 12.0) +
            0.25 * invert_scale(hp_bdry_pct, 6.0, 28.0) +
            0.20 * invert_scale(hp_wsr, 10.0, 36.0) +
            0.18 * anchor_scale(hp_post_b_comp, 15.0, 60.0) +
            0.12 * anchor_scale(hp_dot_pct, 20.0, 55.0)
        ) * (hp_opp / 0.80)
        
        reliability = np.sqrt(np.clip(hp_balls / 80.0, 0.35, 1.0))
        final_phase_score = hp_score * reliability
        
        phase_records.append({
            "phase": ph,
            "player_id": p_id,
            "player_name": p_name,
            "hp_balls": hp_balls,
            "hp_runs": hp_runs,
            "hp_wkts": hp_wkts,
            "hp_econ": hp_econ,
            "hp_wsr": hp_wsr,
            "hp_bdry_pct": hp_bdry_pct,
            "hp_dot_pct": hp_dot_pct,
            "hp_post_b_comp": hp_post_b_comp,
            "phase_score": final_phase_score
        })

ph_df_all = pd.DataFrame(phase_records)
ph_df_all["phase_rank"] = ph_df_all.groupby("phase")["phase_score"].rank(ascending=False, method="min").astype(int)
ph_df_all.sort_values(by=["phase", "phase_rank"], inplace=True)
ph_df_all.to_csv(BOWL_PHASE_CSV, index=False)
print(f"Saved Bowling Phase Specialists to {BOWL_PHASE_CSV}")

best_bowlers_xi = {}
print("\n=== Best Bowlers by Match Phase ===")
for ph in ["Powerplay", "Middle", "Death"]:
    sub = ph_df_all[ph_df_all["phase"] == ph].head(3)
    best_p = sub.iloc[0]
    best_bowlers_xi[ph] = {
        "name": best_p["player_name"],
        "hp_balls": int(best_p["hp_balls"]),
        "econ": round(float(best_p["hp_econ"]), 2),
        "wsr": round(float(best_p["hp_wsr"]), 1),
        "post_b_comp": round(float(best_p["hp_post_b_comp"]), 1),
        "score": round(float(best_p["phase_score"]), 1)
    }
    print(f"\n{ph} Specialists:")
    for _, r in sub.iterrows():
        print(f"  Rank {r['phase_rank']}: {r['player_name']} | HP: {r['hp_balls']}b, Econ: {r['hp_econ']:.2f}, WSR: {r['hp_wsr']:.1f}, Post-Bdry: {r['hp_post_b_comp']:.1f}%, Score: {r['phase_score']:.1f}")

# ============================================================
# 3. ASSEMBLE PRESSURE-PROOF WORLD XI
# ============================================================
world_xi = {
    "batting_lineup": best_batters_xi,
    "bowling_attack": best_bowlers_xi
}
with open(XI_JSON, "w") as f:
    json.dump(world_xi, f, indent=2)

print(f"\nSaved Pressure-Proof World XI to {XI_JSON}")
print("Positional & Phase Analysis completed successfully!")
