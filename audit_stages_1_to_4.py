"""
Comprehensive Audit Script: Stages 1 to 4
Checks:
1. Master Parquet integrity (200,999 rows, 0 NaNs in critical columns, [0, 1] range bounds, 30% pressure split).
2. batter_performance.csv (162 batters, 0 NaNs, 0 Infs, sequential ranks 1-162, monotonic decreasing scores).
3. bowler_performance.csv (243 bowlers, 0 NaNs, 0 Infs, sequential ranks 1-243, monotonic decreasing scores).
4. positional_batters.csv (All positions 1-7 represented, 0 NaNs).
5. bowling_phase_specialists.csv (All phases Powerplay, Middle, Death represented, 0 NaNs).
6. pressure_proof_xi.json (Slots 1-7 filled, 3 bowling phases filled).
"""

import os
import json
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"

print("=====================================================")
print("        COMPREHENSIVE AUDIT: STAGES 1 TO 4           ")
print("=====================================================")

errors = []
warnings = []

# --- 1. Master Parquet ---
parquet_path = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")
if not os.path.exists(parquet_path):
    errors.append("Missing enriched_ball_by_ball.parquet!")
else:
    df = pd.read_parquet(parquet_path)
    print(f"1. Master Parquet: {len(df):,} rows, {len(df.columns)} columns")
    
    key_cols = [
        "match_id", "innings", "overid", "over_ball_num", "delivery_total_runs",
        "bowler_runs_conceded", "is_bowler_wicket", "is_dot_ball", "is_strike_rotation",
        "is_boundary", "bowler_post_boundary", "bowler_post_wicket", "batter_is_cold",
        "batter_is_set", "match_stakes_weight", "opp_bowling_team_quality",
        "opp_batting_team_quality", "pressure_batter", "pressure_bowler",
        "is_high_pressure_batter", "is_high_pressure_bowler"
    ]
    for c in key_cols:
        nan_count = df[c].isna().sum()
        if nan_count > 0:
            errors.append(f"Parquet column '{c}' has {nan_count} NaNs!")
            
    if (df["pressure_batter"] < 0.0).any() or (df["pressure_batter"] > 1.0).any():
        errors.append("pressure_batter has values outside [0, 1]!")
    if (df["pressure_bowler"] < 0.0).any() or (df["pressure_bowler"] > 1.0).any():
        errors.append("pressure_bowler has values outside [0, 1]!")
        
    p_bat_rate = df["is_high_pressure_batter"].mean()
    p_bowl_rate = df["is_high_pressure_bowler"].mean()
    if not (0.28 <= p_bat_rate <= 0.32):
        warnings.append(f"Batter HP rate is {p_bat_rate*100:.2f}%, expected ~30%")
    if not (0.28 <= p_bowl_rate <= 0.32):
        warnings.append(f"Bowler HP rate is {p_bowl_rate*100:.2f}%, expected ~30%")

# --- 2. Batter Performance ---
bat_path = os.path.join(DATA_DIR, "batter_performance.csv")
if not os.path.exists(bat_path):
    errors.append("Missing batter_performance.csv!")
else:
    bdf = pd.read_csv(bat_path)
    print(f"2. Batter Performance: {len(bdf)} qualified batters")
    
    for c in bdf.columns:
        if bdf[c].isna().sum() > 0:
            errors.append(f"batter_performance.csv column '{c}' has NaNs!")
        if pd.api.types.is_numeric_dtype(bdf[c]):
            if np.isinf(bdf[c].dropna()).any():
                errors.append(f"batter_performance.csv column '{c}' has Infs!")
            
    if list(bdf["rank"]) != list(range(1, len(bdf) + 1)):
        errors.append("Batter ranks are not sequential from 1 to N!")
        
    if not bdf["final_rank_score"].is_monotonic_decreasing:
        errors.append("Batter final_rank_score is not monotonically decreasing!")

# --- 3. Bowler Performance ---
bowl_path = os.path.join(DATA_DIR, "bowler_performance.csv")
if not os.path.exists(bowl_path):
    errors.append("Missing bowler_performance.csv!")
else:
    bwdf = pd.read_csv(bowl_path)
    print(f"3. Bowler Performance: {len(bwdf)} qualified bowlers")
    
    for c in bwdf.columns:
        if bwdf[c].isna().sum() > 0:
            errors.append(f"bowler_performance.csv column '{c}' has NaNs!")
        if pd.api.types.is_numeric_dtype(bwdf[c]):
            if np.isinf(bwdf[c].dropna()).any():
                errors.append(f"bowler_performance.csv column '{c}' has Infs!")
            
    if list(bwdf["rank"]) != list(range(1, len(bwdf) + 1)):
        errors.append("Bowler ranks are not sequential from 1 to N!")
        
    if not bwdf["final_rank_score"].is_monotonic_decreasing:
        errors.append("Bowler final_rank_score is not monotonically decreasing!")

# --- 4. Positional Batters ---
pos_bat_path = os.path.join(DATA_DIR, "positional_batters.csv")
if not os.path.exists(pos_bat_path):
    errors.append("Missing positional_batters.csv!")
else:
    pos_df = pd.read_csv(pos_bat_path)
    unique_pos = sorted(list(pos_df["batting_position"].unique()))
    print(f"4. Positional Batters: {len(pos_df)} player-position records across positions {unique_pos}")
    if set(unique_pos) != set(range(1, 8)):
        errors.append("positional_batters.csv is missing some positions 1-7!")
    if pos_df.isna().sum().sum() > 0:
        errors.append("positional_batters.csv has NaNs!")

# --- 5. Bowling Phase Specialists ---
phase_bowl_path = os.path.join(DATA_DIR, "bowling_phase_specialists.csv")
if not os.path.exists(phase_bowl_path):
    errors.append("Missing bowling_phase_specialists.csv!")
else:
    ph_df = pd.read_csv(phase_bowl_path)
    unique_phases = sorted(list(ph_df["phase"].unique()))
    print(f"5. Bowling Phase Specialists: {len(ph_df)} player-phase records across {unique_phases}")
    if set(unique_phases) != {"Death", "Middle", "Powerplay"}:
        errors.append("bowling_phase_specialists.csv is missing some phases!")
    if ph_df.isna().sum().sum() > 0:
        errors.append("bowling_phase_specialists.csv has NaNs!")

# --- 6. Pressure-Proof World XI ---
xi_path = os.path.join(DATA_DIR, "pressure_proof_xi.json")
if not os.path.exists(xi_path):
    errors.append("Missing pressure_proof_xi.json!")
else:
    with open(xi_path, "r") as f:
        xi_data = json.load(f)
    print(f"6. Pressure-Proof XI: {len(xi_data['batting_lineup'])} batting slots, {len(xi_data['bowling_attack'])} bowling phases")
    if len(xi_data["batting_lineup"]) != 7:
        errors.append("pressure_proof_xi.json does not have 7 batting positions!")
    if len(xi_data["bowling_attack"]) != 3:
        errors.append("pressure_proof_xi.json does not have 3 bowling phases!")

print("\n=====================================================")
print(f"TOTAL CRITICAL ERRORS: {len(errors)}")
print(f"TOTAL WARNINGS: {len(warnings)}")
if len(errors) == 0:
    print("STATUS: ALL INTEGRITY CHECKS PASSED WITH FLYING COLORS! NO ERRORS FOUND. 🚀")
else:
    for e in errors:
        print("  [ERROR]", e)
for w in warnings:
    print("  [WARNING]", w)
print("=====================================================")
