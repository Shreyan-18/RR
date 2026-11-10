"""
SupeRR Selector Season 2 - Fully Calibrated Stage 2: Context, Stakes, Rivalry & Global Fortresses
Expands Fortresses:
- International Fortresses:
  * Australia in Aus (0.15) - Bouncy tracks, huge MCG/Optus boundaries, hostile Aussie crowd
  * India in Ind (0.15) - 50k-100k deafening home crowd, turning conditions
  * England in UK (0.15) - Hostile English crowd (Barmy Army, Western Terrace), swinging conditions
  * New Zealand in NZ (0.14) - Unique drop-in pitches, Wellington wind, Eden Park dimensions
  * South Africa in SA (0.14) - High altitude bounce at Wanderers/Centurion, intimidating pace
  * Pakistan in Pak (0.13) - Rawalpindi, Gaddafi, National Stadium passionate crowds
  * Bangladesh in Ban (0.12) - Treacherous Mirpur spinning fortress, fanatic local crowd
  * West Indies in WI (0.12) - Kensington Oval, Guyana, Sabina Park calypso pressure
  * Sri Lanka in SL (0.10) - R. Premadasa, Galle turning tracks, extreme humidity
- IPL Franchises:
  * Top IPL Fortresses: GT (Ahmedabad 100k+), CSK (Chepauk yellow wall), MI (Wankhede), RCB (Chinnaswamy decibels) -> 0.10
  * Historic IPL Fortresses: KKR (Eden Gardens 66k), RR, SRH, LSG, DC, PBKS -> 0.08
  * Neutral venues (UAE, Oman, Qatar, USA) -> 0.00
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
PARQUET_PATH = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")

print("--- Fully Calibrated Stage 2: Context, Stakes, Rivalry & Global Fortresses ---")
print("Loading data...")
df = pd.read_parquet(PARQUET_PATH)
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
teams = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))

# --- 1. Chronological Series Tracking (Deciders vs Dead Rubbers) ---
matches["match_date"] = pd.to_datetime(matches["match_date"])
matches.sort_values(by=["comp_id", "match_date", "match_id"], inplace=True)

decider_match_ids = set()
dead_rubber_match_ids = set()

for comp_id, g in matches.groupby("comp_id"):
    total_m = len(g)
    if total_m in [3, 5]:
        wins = {}
        threshold = (total_m // 2) + 1  # 2 for 3-match, 3 for 5-match
        for i, (idx, row) in enumerate(g.iterrows()):
            # Check if series was ALREADY clinched prior to this match
            if any(cnt >= threshold for cnt in wins.values()):
                dead_rubber_match_ids.add(row["match_id"])
            
            # Check if this is the final match and it's currently tied
            if i == total_m - 1:
                win_counts = list(wins.values())
                if len(win_counts) == 2 and win_counts[0] == win_counts[1]:
                    decider_match_ids.add(row["match_id"])
            
            w_team = row["win_team_id"]
            if pd.notna(w_team):
                wins[w_team] = wins.get(w_team, 0) + 1

print(f"Identified {len(decider_match_ids)} Tied Series Deciders!")
print(f"Identified {len(dead_rubber_match_ids)} Dead Rubbers (series already won)!")

# --- 2. Marquee High-Ego Rivalry Detection ---
rivalry_pairs = [
    {"Chennai Super Kings", "Mumbai Indians"},
    {"Royal Challengers Bengaluru", "Chennai Super Kings"},
    {"Royal Challengers Bengaluru", "Mumbai Indians"},
    {"India", "Pakistan"},
    {"Australia", "England"},
    {"India", "Australia"}
]

def check_marquee_rivalry(row):
    teams_set = {str(row.get("home_team")), str(row.get("away_team"))}
    return any(teams_set == r for r in rivalry_pairs)

matches = matches.merge(comps[["comp_id", "comp_name", "match_format"]], on="comp_id", how="left")
matches["is_marquee_rivalry"] = matches.apply(check_marquee_rivalry, axis=1)
print(f"Identified {matches['is_marquee_rivalry'].sum()} Marquee High-Ego Rivalry matches!")

# --- 3. Compute Enhanced Match Stakes (W_M) ---
def compute_match_stakes(row):
    m_id = row.get("match_id")
    stage = str(row.get("stage", ""))
    m_num = row.get("match_number")
    is_ko = row.get("knock_out", 0)
    is_riv = row.get("is_marquee_rivalry", False)
    
    # 1. Knockouts / Finals
    if stage == "Final":
        base_w = 1.00
    elif stage in ["Semi Final", "Eliminator"]:
        base_w = 0.95
    elif stage in ["Qualifier"]:
        base_w = 0.90
    elif stage in ["Super 4"]:
        base_w = 0.85
    elif is_ko == 1:
        base_w = 0.90
    # 2. Tied Series Decider
    elif m_id in decider_match_ids:
        base_w = 0.85
    # 3. Dead Rubber (Clinched Series)
    elif m_id in dead_rubber_match_ids:
        base_w = 0.35
    # 4. Late League Games (IPL Match 55+)
    elif "IPL" in str(row.get("comp_name", "")) and pd.notna(m_num) and m_num >= 55:
        base_w = 0.70
    else:
        base_w = 0.50
        
    # High-Ego Marquee Rivalry boost (+0.15, max 1.00)
    if is_riv and m_id not in dead_rubber_match_ids:
        base_w = min(1.00, base_w + 0.15)
        
    return base_w

matches["match_stakes_weight"] = matches.apply(compute_match_stakes, axis=1)

# --- 4. Comprehensive Global Fortress & Backyard Hostility (H_fortress) ---
def compute_comprehensive_fortress(row):
    home = str(row.get("home_team"))
    venue = str(row.get("venue_country"))
    
    # 1. International Fortresses
    if home == "Australia" and venue == "Australia":
        return 0.15, "Australia in Aus"
    if home == "India" and venue == "India":
        return 0.15, "India in Ind"
    if home == "England" and venue in ["United Kingdom", "England"]:
        return 0.15, "England in UK"
    if home == "New Zealand" and venue == "New Zealand":
        return 0.14, "New Zealand in NZ"
    if home == "South Africa" and venue == "South Africa":
        return 0.14, "South Africa in SA"
    if home == "Pakistan" and venue == "Pakistan":
        return 0.13, "Pakistan in Pak"
    if home == "Bangladesh" and venue == "Bangladesh":
        return 0.12, "Bangladesh in Ban"
    if home == "West Indies" and venue == "West Indies":
        return 0.12, "West Indies in WI"
    if home == "Sri Lanka" and venue == "Sri Lanka":
        return 0.10, "Sri Lanka in SL"
        
    # 2. IPL Iconic Home Fortresses
    if venue == "India":
        if home in ["Gujarat Titans", "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bengaluru"]:
            return 0.10, f"{home} Fortress"
        if home in ["Kolkata Knight Riders", "Rajasthan Royals", "Sunrisers Hyderabad", "Lucknow Super Giants", "Delhi Capitals", "Punjab Kings"]:
            return 0.08, f"{home} Fortress"
            
    return 0.00, "Neutral / Standard"

fort_res = matches.apply(compute_comprehensive_fortress, axis=1)
matches["fortress_hostility"] = [r[0] for r in fort_res]
matches["fortress_type"] = [r[1] for r in fort_res]

print(f"Total matches featuring a Fortress: {(matches['fortress_hostility'] > 0).sum()} of {len(matches)}")

# --- 5. Opposition Quality Tiers (Q_opp) ---
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

# --- 6. Merge Back into Deliveries ---
print("Updating deliveries with comprehensive fortress mapping...")
clean_cols = [
    "match_stakes_weight", "is_tied_series_decider", "is_dead_rubber",
    "is_marquee_rivalry", "fortress_hostility", "fortress_type",
    "batter_fortress_pressure", "bowler_fortress_pressure",
    "batter_macro_stakes", "bowler_macro_stakes"
]
for col in clean_cols:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

match_stakes_dict = matches.set_index("match_id")["match_stakes_weight"].to_dict()
match_fortress_dict = matches.set_index("match_id")["fortress_hostility"].to_dict()
match_fortress_type_dict = matches.set_index("match_id")["fortress_type"].to_dict()
match_rivalry_dict = matches.set_index("match_id")["is_marquee_rivalry"].to_dict()
home_team_dict = matches.set_index("match_id")["home_team"].to_dict()

df["match_stakes_weight"] = df["match_id"].map(match_stakes_dict).fillna(0.50)
df["is_tied_series_decider"] = df["match_id"].isin(decider_match_ids)
df["is_dead_rubber"] = df["match_id"].isin(dead_rubber_match_ids)
df["is_marquee_rivalry"] = df["match_id"].map(match_rivalry_dict).fillna(False)

# Fortress advantage applies to VISITING / AWAY team players
df["match_home_team"] = df["match_id"].map(home_team_dict)
df["is_batter_visiting"] = df["batting_team_name"] != df["match_home_team"]
df["is_bowler_visiting"] = df["bowling_team_name"] != df["match_home_team"]

df["fortress_boost"] = df["match_id"].map(match_fortress_dict).fillna(0.0)
df["fortress_type"] = df["match_id"].map(match_fortress_type_dict).fillna("Neutral")
df["batter_fortress_pressure"] = np.where(df["is_batter_visiting"], df["fortress_boost"], 0.0)
df["bowler_fortress_pressure"] = np.where(df["is_bowler_visiting"], df["fortress_boost"], 0.0)

# Opposition quality
df["opp_bowling_team_quality"] = df["bowling_team_name"].map(team_quality_map).fillna(DEFAULT_QUALITY)
df["opp_batting_team_quality"] = df["batting_team_name"].map(team_quality_map).fillna(DEFAULT_QUALITY)

# Composite Macro Stakes Factor
df["batter_macro_stakes"] = np.clip(
    0.50 * df["match_stakes_weight"] + 0.35 * df["opp_bowling_team_quality"] + 0.15 * df["batter_fortress_pressure"],
    0.0, 1.0
)
df["bowler_macro_stakes"] = np.clip(
    0.50 * df["match_stakes_weight"] + 0.35 * df["opp_batting_team_quality"] + 0.15 * df["bowler_fortress_pressure"],
    0.0, 1.0
)

print(f"Saving enriched parquet to {PARQUET_PATH}...")
df.to_parquet(PARQUET_PATH, index=False)

print("\n=== Comprehensive Global Fortresses Verified ===")
print("Fortress Breakdown across Matches:")
print(matches["fortress_type"].value_counts().head(15))
print("\nDeliveries where visiting batter faced a fortress:", (df["batter_fortress_pressure"] > 0).sum())
print("Deliveries where visiting bowler faced a fortress:", (df["bowler_fortress_pressure"] > 0).sum())
print("Stage 2 fully updated and saved successfully!")
