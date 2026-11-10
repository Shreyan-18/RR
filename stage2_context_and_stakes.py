"""
SupeRR Selector Season 2 - Stage 2: Context & Stakes Modeling
Calculates:
1. Match Stakes (W_M): Finals, Knockouts, Bilateral Tied Series Deciders (1-1, 2-2), Late League Games.
2. Opposition Quality Tiers (Q_opp): Tier 1 (India=1.00), Tier 1.5 (IPL), Tier 2 (Eng/Aus/SA/NZ=0.85),
   Tier 3 (Pak/WI/SL/Afg=0.70), Tier 4 (Ban/Ire/Zim/Ned/Sco/USA=0.55), Tier 5 (Associates=0.40).
3. Pre-ball Context Factor: C_match = 0.60 * W_M + 0.40 * Q_opp
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
PARQUET_PATH = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")

print("--- Stage 2: Context & Stakes Modeling ---")
print("Loading enriched deliveries...")
df = pd.read_parquet(PARQUET_PATH)
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
teams = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))

# --- 1. Detect Tied Bilateral Series Deciders ---
matches["match_date"] = pd.to_datetime(matches["match_date"])
matches.sort_values(by=["comp_id", "match_date", "match_id"], inplace=True)

decider_match_ids = set()
for comp_id, g in matches.groupby("comp_id"):
    if len(g) in [3, 5]:
        wins = {}
        for i, (idx, row) in enumerate(g.iterrows()):
            w_team = row["win_team_id"]
            if i == len(g) - 1:  # Final match of series
                win_counts = list(wins.values())
                # Tied going into final match (e.g., [1, 1] in 3-match or [2, 2] in 5-match)
                if len(win_counts) == 2 and win_counts[0] == win_counts[1]:
                    decider_match_ids.add(row["match_id"])
            if pd.notna(w_team):
                wins[w_team] = wins.get(w_team, 0) + 1

print(f"Identified {len(decider_match_ids)} tied bilateral series deciders!")

# --- 2. Calculate Match Stakes Weight (W_M) ---
def compute_match_stakes(row):
    stage = str(row.get("stage", ""))
    m_id = row.get("match_id")
    m_num = row.get("match_number")
    is_ko = row.get("knock_out", 0)
    
    # Official Knockout Stages
    if stage == "Final":
        return 1.00
    if stage in ["Semi Final", "Eliminator"]:
        return 0.95
    if stage in ["Qualifier"]:
        return 0.90
    if stage in ["Super 4"]:
        return 0.85
    if is_ko == 1:
        return 0.90
        
    # Tied Series Deciders
    if m_id in decider_match_ids:
        return 0.85
        
    # Late League Games (IPL match 55+ where qualification is on the line)
    comp_name = str(row.get("comp_name", ""))
    if "IPL" in comp_name and pd.notna(m_num) and m_num >= 55:
        return 0.70
        
    # Baseline League / Group stage
    return 0.50

# Apply to matches
matches = matches.merge(comps[["comp_id", "comp_name", "match_format"]], on="comp_id", how="left")
matches["match_stakes_weight"] = matches.apply(compute_match_stakes, axis=1)

# --- 3. Opposition Quality Tier Calibration (Q_opp) ---
# Calibrated on 2022-2026 performance & user hierarchy:
# Tier 1: India (Rank 1) -> 1.00
# Tier 1.5: IPL Franchises -> 0.90
# Tier 2: Eng, Aus, SA, NZ (Rank 2) -> 0.85
# Tier 3: Pak, WI, SL, Afg (Rank 3) -> 0.70
# Tier 4: Ban, Ire, Zim, Ned, Sco, USA (Rank 4) -> 0.55
# Tier 5: Other Associates & A-teams (Rank 5) -> 0.40

team_quality_map = {
    # Tier 1 (Rank 1 - India dominant with 82 T20I wins, 2 WCs)
    "India": 1.00,
    
    # Tier 1.5 (IPL Franchises - concentrated international star power)
    "Gujarat Titans": 0.92, "Chennai Super Kings": 0.90, "Mumbai Indians": 0.90,
    "Royal Challengers Bengaluru": 0.90, "Rajasthan Royals": 0.90, "Kolkata Knight Riders": 0.90,
    "Sunrisers Hyderabad": 0.88, "Lucknow Super Giants": 0.88, "Delhi Capitals": 0.88, "Punjab Kings": 0.86,
    
    # Tier 2 (Rank 2 - Traditional powerhouses)
    "Australia": 0.85, "England": 0.85, "South Africa": 0.85, "New Zealand": 0.85,
    
    # Tier 3 (Rank 3 - Strong competitive full members)
    "Pakistan": 0.75, "West Indies": 0.70, "Sri Lanka": 0.68, "Afghanistan": 0.68,
    
    # Tier 4 (Rank 4 - Emerging full members / top associates)
    "Bangladesh": 0.58, "Ireland": 0.55, "Zimbabwe": 0.55, "Netherlands": 0.52,
    "Scotland": 0.52, "United States Of America": 0.50,
    
    # Tier 5 (Rank 5 - Emerging Associates / A-Teams)
    "United Arab Emirates": 0.40, "Namibia": 0.40, "Nepal": 0.40, "Oman": 0.40,
    "Canada": 0.38, "Hong Kong": 0.38, "Kuwait": 0.35, "Singapore": 0.35, "Japan": 0.30,
    "India A": 0.45, "Pakistan A": 0.42, "Sri Lanka A": 0.40, "Bangladesh A": 0.40, "Afghanistan A": 0.40
}
DEFAULT_QUALITY = 0.40

# Map match_stakes_weight into df
df.drop(columns=[col for col in ["match_stakes_weight", "is_tied_series_decider"] if col in df.columns], inplace=True)
match_stakes_dict = matches.set_index("match_id")["match_stakes_weight"].to_dict()
df["match_stakes_weight"] = df["match_id"].map(match_stakes_dict).fillna(0.50)
df["is_tied_series_decider"] = df["match_id"].isin(decider_match_ids)

# Map opposition quality
# For batter: quality of bowling team faced
df["opp_bowling_team_quality"] = df["bowling_team_name"].map(team_quality_map).fillna(DEFAULT_QUALITY)
# For bowler: quality of batting team faced
df["opp_batting_team_quality"] = df["batting_team_name"].map(team_quality_map).fillna(DEFAULT_QUALITY)

# Context Macro-Factor (C_macro)
df["batter_macro_stakes"] = 0.60 * df["match_stakes_weight"] + 0.40 * df["opp_bowling_team_quality"]
df["bowler_macro_stakes"] = 0.60 * df["match_stakes_weight"] + 0.40 * df["opp_batting_team_quality"]

# Save updated parquet
print(f"Saving updated enriched deliveries with Stage 2 features to {PARQUET_PATH}...")
df.to_parquet(PARQUET_PATH, index=False)

# Summary inspection
print("\n=== Stage 2 Modeling Breakdown ===")
print("Match Stakes Weight Distribution:")
print(matches["match_stakes_weight"].value_counts().sort_index(ascending=False))

print("\nSample Tied Series Deciders:")
deciders_sample = matches[matches["match_id"].isin(decider_match_ids)][["match_id", "comp_name", "home_team", "away_team", "result"]].head(5)
print(deciders_sample)

print("\nOpposition Quality Tiers Sample:")
for t in ["India", "Australia", "Pakistan", "Gujarat Titans", "Bangladesh", "Nepal"]:
    print(f"  {t}: {team_quality_map.get(t)}")

print("\nStage 2 completed successfully!")
