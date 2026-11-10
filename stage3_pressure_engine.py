"""
SupeRR Selector Season 2 - Stage 3: Ball-Level Pressure Engine
Calculates:
1. Batter Pressure Index (P_batter in [0, 1]) combining Macro Stakes, Chasing/Setting Situational State,
   and Batter Psychological/Momentum factors.
2. Bowler Pressure Index (P_bowler in [0, 1]) combining Macro Stakes, Closeness/Death Defending State,
   and Bowler Post-Boundary/Post-Wicket Momentum.
3. Pressure Split: 70th percentile thresholding into High-Pressure vs Normal Conditions.
"""

import os
import json
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
PARQUET_PATH = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")
OUTPUT_SUMMARY = os.path.join(DATA_DIR, "stage3_summary.json")

print("--- Stage 3: Executing Ball-Level Pressure Engine ---")
df = pd.read_parquet(PARQUET_PATH)
print(f"Loaded deliveries: {len(df):,}")

# ============================================================
# 1. BATTER SITUATIONAL & PSYCHOLOGICAL PRESSURE (P_batter)
# ============================================================
print("1. Computing Batter Pressure Index...")

# A. Innings 2 (The Chase)
rrr_clipped = np.clip(df["rrr"] / 16.0, 0.0, 1.0).fillna(0.5)
rrr_diff = np.clip((df["rrr"] - df["crr"]) / 6.0, 0.0, 1.0).fillna(0.0)
wkt_factor_bat = np.clip(df["cum_wickets_before"] / 9.0, 0.0, 1.0)
balls_exhaust_bat = 1.0 - (df["balls_left_before"] / 120.0)

s_chase_bat = (
    0.40 * rrr_clipped +
    0.25 * wkt_factor_bat +
    0.20 * balls_exhaust_bat +
    0.15 * rrr_diff
)

# B. Innings 1 (Target Setting)
phase_weight_bat = df["phase"].map({"Powerplay": 0.45, "Middle": 0.35, "Death": 0.85}).fillna(0.35)
collapse_weight_bat = np.clip(df["cum_wickets_before"] / 6.0, 0.0, 1.0)
s_set_bat = 0.55 * phase_weight_bat + 0.45 * collapse_weight_bat

s_base_bat = np.where(df["innings"] == 2, s_chase_bat, s_set_bat)

# C. Batter Psychological & Form Layer
bat_psych = (
    np.where(df["batter_is_cold"], 0.12, 0.0) +
    np.where(df["batter_is_set"], -0.10, 0.0) +
    np.where(df["bowler_post_wicket"], 0.15, 0.0) +
    np.where(df["batter_post_boundary"], -0.08, 0.0) +
    np.where(df["dot_pressure_building"], 0.10, 0.0) +
    np.where(df["batter_in_slump"], 0.08, 0.0) +
    np.where(df["batter_in_form"], -0.06, 0.0)
)
s_micro_bat = np.clip(s_base_bat + bat_psych, 0.0, 1.0)

# D. Composite Batter Pressure
p_bat = 0.40 * df["batter_macro_stakes"] + 0.60 * s_micro_bat
# Super Over hardcoded to 1.00 max pressure
p_bat = np.where(df["is_super_over"], 1.00, p_bat)
df["pressure_batter"] = np.clip(p_bat, 0.0, 1.0)

# ============================================================
# 2. BOWLER SITUATIONAL & PSYCHOLOGICAL PRESSURE (P_bowler)
# ============================================================
print("2. Computing Bowler Pressure Index...")

# A. Innings 2 (Defending Target)
phase_bowl_weight = df["phase"].map({"Powerplay": 0.45, "Middle": 0.50, "Death": 0.85}).fillna(0.50)
closeness_bowl = np.exp(-((df["rrr"].fillna(9.0) - 9.0) ** 2) / 25.0)
wkt_threat_bowl = 1.0 - np.clip(df["cum_wickets_before"] / 10.0, 0.0, 1.0)

s_chase_bowl = (
    0.45 * phase_bowl_weight +
    0.35 * closeness_bowl +
    0.20 * wkt_threat_bowl
)

# B. Innings 1 (First Innings Containment & Death Bowling)
s_set_bowl = df["phase"].map({"Powerplay": 0.50, "Middle": 0.35, "Death": 0.80}).fillna(0.35)
s_base_bowl = np.where(df["innings"] == 2, s_chase_bowl, s_set_bowl)

# C. Bowler Psychological & Micro-Momentum Layer
bowl_psych = (
    np.where(df["bowler_post_boundary"], 0.20, 0.0) +   # Conceded boundary on previous ball!
    np.where(df["bowler_post_wicket"], -0.15, 0.0) +    # High confidence after wicket
    np.where(df["bowler_in_slump"], 0.08, 0.0) +
    np.where(df["bowler_in_form"], -0.06, 0.0)
)
s_micro_bowl = np.clip(s_base_bowl + bowl_psych, 0.0, 1.0)

# D. Composite Bowler Pressure
p_bowl = 0.40 * df["bowler_macro_stakes"] + 0.60 * s_micro_bowl
p_bowl = np.where(df["is_super_over"], 1.00, p_bowl)
df["pressure_bowler"] = np.clip(p_bowl, 0.0, 1.0)

# ============================================================
# 3. PRESSURE SPLIT (70th PERCENTILE THRESHOLD)
# ============================================================
print("3. Executing Pressure Split (70th Percentile Cut-off)...")
thresh_bat = float(np.percentile(df["pressure_batter"], 70))
thresh_bowl = float(np.percentile(df["pressure_bowler"], 70))

df["is_high_pressure_batter"] = df["pressure_batter"] >= thresh_bat
df["is_high_pressure_bowler"] = df["pressure_bowler"] >= thresh_bowl

print(f"  Batter 70th Percentile Threshold: {thresh_bat:.4f}")
print(f"  Bowler 70th Percentile Threshold: {thresh_bowl:.4f}")
print(f"  High-Pressure Batter Deliveries: {df['is_high_pressure_batter'].sum():,} ({df['is_high_pressure_batter'].mean()*100:.1f}%)")
print(f"  High-Pressure Bowler Deliveries: {df['is_high_pressure_bowler'].sum():,} ({df['is_high_pressure_bowler'].mean()*100:.1f}%)")

# ============================================================
# 4. DATA INTEGRITY & SANITY AUDIT
# ============================================================
print("\n--- Running Stage 3 Integrity Audit ---")
for col in ["pressure_batter", "pressure_bowler", "is_high_pressure_batter", "is_high_pressure_bowler"]:
    n_nan = df[col].isna().sum()
    print(f"  {col}: {n_nan} NaNs (dtype: {df[col].dtype})")
    assert n_nan == 0, f"Error: {col} has {n_nan} NaNs!"

# Save updated dataset
print(f"\nSaving updated enriched parquet to {PARQUET_PATH}...")
df.to_parquet(PARQUET_PATH, index=False)

# Diagnostics summary
summary = {
    "total_balls": int(len(df)),
    "thresh_bat": thresh_bat,
    "thresh_bowl": thresh_bowl,
    "high_pressure_bat_balls": int(df["is_high_pressure_batter"].sum()),
    "high_pressure_bowl_balls": int(df["is_high_pressure_bowler"].sum()),
    "death_overs_bat_hp_pct": float(df[df["phase"] == "Death"]["is_high_pressure_batter"].mean()),
    "death_overs_bowl_hp_pct": float(df[df["phase"] == "Death"]["is_high_pressure_bowler"].mean()),
    "post_boundary_bowl_hp_pct": float(df[df["bowler_post_boundary"]]["is_high_pressure_bowler"].mean()),
    "decider_matches_bat_hp_pct": float(df[df["is_tied_series_decider"]]["is_high_pressure_batter"].mean())
}

with open(OUTPUT_SUMMARY, "w") as f:
    json.dump(summary, f, indent=2)

print("\nStage 3 completed successfully!")
print("Key Validation Findings:")
print(f"  Death Overs Batter High-Pressure Rate: {summary['death_overs_bat_hp_pct']*100:.1f}%")
print(f"  Death Overs Bowler High-Pressure Rate: {summary['death_overs_bowl_hp_pct']*100:.1f}%")
print(f"  Post-Boundary Deliveries Bowler High-Pressure Rate: {summary['post_boundary_bowl_hp_pct']*100:.1f}%")
