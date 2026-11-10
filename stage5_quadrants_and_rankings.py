"""
SupeRR Selector Season 2 - Stage 5: 4-Quadrant Permutations Model & Official Rankings
Calculates:
1. 4-Quadrant Player Segmentation across Normal Score vs. High-Pressure Score:
   - Q1: Clutch Giants (High Normal, High Pressure)
   - Q2: Crisis Specialists (Low/Mid Normal, High Pressure)
   - Q3: Front-Runners (High Normal, Low Pressure)
   - Q4: Strugglers (Low Normal, Low Pressure)
2. Exports:
   - batter_quadrants.csv
   - bowler_quadrants.csv
   - top10_batters.csv
   - top10_bowlers.csv
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
BAT_CSV = os.path.join(DATA_DIR, "batter_performance.csv")
BOWL_CSV = os.path.join(DATA_DIR, "bowler_performance.csv")
BAT_QUAD_CSV = os.path.join(DATA_DIR, "batter_quadrants.csv")
BOWL_QUAD_CSV = os.path.join(DATA_DIR, "bowler_quadrants.csv")
TOP10_BAT_CSV = os.path.join(DATA_DIR, "top10_batters.csv")
TOP10_BOWL_CSV = os.path.join(DATA_DIR, "top10_bowlers.csv")

print("--- Stage 5: 4-Quadrant Permutations & Official Rankings ---")
bdf = pd.read_csv(BAT_CSV)
bwdf = pd.read_csv(BOWL_CSV)

# ============================================================
# 1. BATTER 4-QUADRANT PERMUTATIONS MODEL
# ============================================================
print("\n1. Classifying Batters into 4 Archetypes...")
med_norm_bat = float(bdf["norm_score"].median())
med_hp_bat = float(bdf["hp_score"].median())

def assign_batter_quadrant(row):
    is_high_norm = row["norm_score"] >= med_norm_bat
    is_high_hp = row["hp_score"] >= med_hp_bat
    
    if is_high_norm and is_high_hp:
        return "Quadrant 1: Clutch Giants", "All-Condition Master (Dominant in normal & pressure)"
    elif not is_high_norm and is_high_hp:
        return "Quadrant 2: Crisis Specialists", "Crisis Men (Elevates significantly under pressure)"
    elif is_high_norm and not is_high_hp:
        return "Quadrant 3: Front-Runners", "Flat-Track Accumulator (Thrives when easy, dips under pressure)"
    else:
        return "Quadrant 4: Strugglers", "Inconsistent Performer (Low impact across both)"

res_bat = bdf.apply(assign_batter_quadrant, axis=1)
bdf["quadrant"] = [r[0] for r in res_bat]
bdf["archetype_desc"] = [r[1] for r in res_bat]

bdf.to_csv(BAT_QUAD_CSV, index=False)
print(f"Saved Batter Quadrants to {BAT_QUAD_CSV}")

print(f"Batter Medians: Normal Score = {med_norm_bat:.2f}, High-Pressure Score = {med_hp_bat:.2f}")
print("Batter Quadrant Counts:")
print(bdf["quadrant"].value_counts())

# Top 10 Batters Export
top10_bat = bdf.head(10).copy()
top10_bat.to_csv(TOP10_BAT_CSV, index=False)
print(f"Saved Top 10 Batters to {TOP10_BAT_CSV}")

# ============================================================
# 2. BOWLER 4-QUADRANT PERMUTATIONS MODEL
# ============================================================
print("\n2. Classifying Bowlers into 4 Archetypes...")
med_norm_bowl = float(bwdf["norm_score"].median())
med_hp_bowl = float(bwdf["hp_score"].median())

def assign_bowler_quadrant(row):
    is_high_norm = row["norm_score"] >= med_norm_bowl
    is_high_hp = row["hp_score"] >= med_hp_bowl
    
    if is_high_norm and is_high_hp:
        return "Quadrant 1: Clutch Giants", "All-Condition Master (Dominant in normal & pressure)"
    elif not is_high_norm and is_high_hp:
        return "Quadrant 2: Crisis Specialists", "Crisis Men (Elevates significantly under pressure)"
    elif is_high_norm and not is_high_hp:
        return "Quadrant 3: Front-Runners", "Flat-Track Accumulator (Thrives when easy, dips under pressure)"
    else:
        return "Quadrant 4: Strugglers", "Inconsistent Performer (Low impact across both)"

res_bowl = bwdf.apply(assign_bowler_quadrant, axis=1)
bwdf["quadrant"] = [r[0] for r in res_bowl]
bwdf["archetype_desc"] = [r[1] for r in res_bowl]

bwdf.to_csv(BOWL_QUAD_CSV, index=False)
print(f"Saved Bowler Quadrants to {BOWL_QUAD_CSV}")

print(f"Bowler Medians: Normal Score = {med_norm_bowl:.2f}, High-Pressure Score = {med_hp_bowl:.2f}")
print("Bowler Quadrant Counts:")
print(bwdf["quadrant"].value_counts())

# Top 10 Bowlers Export
top10_bowl = bwdf.head(10).copy()
top10_bowl.to_csv(TOP10_BOWL_CSV, index=False)
print(f"Saved Top 10 Bowlers to {TOP10_BOWL_CSV}")

# ============================================================
# 3. SAMPLE ARCHETYPE BREAKDOWN
# ============================================================
print("\n=== Sample Batters in Each Quadrant ===")
for q in sorted(bdf["quadrant"].unique()):
    sample = bdf[bdf["quadrant"] == q].head(3)
    print(f"\n{q}:")
    for _, r in sample.iterrows():
        print(f"  {r['player_name']} | Normal Score: {r['norm_score']:.1f}, HP Score: {r['hp_score']:.1f}, PPR: {r['ppr']:.2f}")

print("\n=== Sample Bowlers in Each Quadrant ===")
for q in sorted(bwdf["quadrant"].unique()):
    sample = bwdf[bwdf["quadrant"] == q].head(3)
    print(f"\n{q}:")
    for _, r in sample.iterrows():
        print(f"  {r['player_name']} | Normal Score: {r['norm_score']:.1f}, HP Score: {r['hp_score']:.1f}, PPR: {r['ppr']:.2f}")

print("\nStage 5 Quadrant Classification completed successfully!")
