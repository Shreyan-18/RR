"""
SupeRR Selector Season 2 - Step 1: Data Ingestion & Game-State Reconstruction
Ingests, cleans, links, and enriches ball_by_ball data with live game-states,
match context stakes, opponent quality tiers, and bowler post-boundary signals.
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
OUTPUT_PARQUET = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")
OUTPUT_SUMMARY = os.path.join(DATA_DIR, "ingestion_summary.json")

print("--- Step 1: Loading Raw Data ---")
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
teams = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))
mapping = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))
bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"))

print(f"Competitions: {len(comps):,}")
print(f"Matches: {len(matches):,}")
print(f"Teams: {len(teams):,}")
print(f"Player Mappings: {len(mapping):,}")
print(f"Deliveries: {len(bbb):,}")

# --- 1. Team Strength Tiers & Quality Ranks ---
team_rank_map = {
    # Tier 1 (Rank 1.0)
    "India": 1.0,
    # Tier 2 (Rank 1.25)
    "England": 1.25, "Australia": 1.25, "South Africa": 1.25, "New Zealand": 1.25,
    # Tier 3 (Rank 1.50)
    "Pakistan": 1.50, "West Indies": 1.50, "Sri Lanka": 1.50, "Afghanistan": 1.50,
    # Tier 4 (Rank 1.80)
    "Bangladesh": 1.80, "Ireland": 1.80, "Zimbabwe": 1.80, "Netherlands": 1.80,
    "Scotland": 1.80, "United States Of America": 1.80,
    # IPL Elite Franchise Tier (Rank 1.30 - 1.45)
    "Chennai Super Kings": 1.30, "Mumbai Indians": 1.30, "Gujarat Titans": 1.35,
    "Kolkata Knight Riders": 1.35, "Rajasthan Royals": 1.35, "Sunrisers Hyderabad": 1.40,
    "Royal Challengers Bengaluru": 1.40, "Delhi Capitals": 1.45, "Lucknow Super Giants": 1.45,
    "Punjab Kings": 1.50
}
DEFAULT_RANK = 2.0  # Associate / A-teams

# Team ID to Name mapping
team_dict = teams.drop_duplicates(subset=["team_id"]).set_index("team_id")["team_name"].to_dict()

# --- 2. Match Stakes & Must-Win Game Detection ---
print("\n--- Identifying Match Stakes & Series Deciders ---")
stage_stakes = {
    "Final": 1.00,
    "Semi Final": 0.95,
    "Eliminator": 0.95,
    "Qualifier": 0.90,
    "Super 4": 0.80,
    "League": 0.50,
    "Others": 0.50
}
matches["stage_weight"] = matches["stage"].map(stage_stakes).fillna(0.50)
matches.loc[matches["knock_out"] == 1, "stage_weight"] = np.maximum(matches["stage_weight"], 0.90)

# Detect Must-Win Series Deciders in Bilateral Series:
# If series has 3 or 5 matches, and this is the final scheduled match in a tied series
matches["match_date"] = pd.to_datetime(matches["match_date"])
matches.sort_values(by=["comp_id", "match_date", "match_id"], inplace=True)

matches["is_series_decider"] = False
for comp_id, group in matches.groupby("comp_id"):
    if len(group) in [3, 5]:
        # Check if bilateral series
        c_format = comps.loc[comps["comp_id"] == comp_id, "match_format"].values
        if len(c_format) > 0 and c_format[0] == "T20I":
            # The final match is potentially a decider
            final_match_idx = group.index[-1]
            matches.loc[final_match_idx, "is_series_decider"] = True
            matches.loc[final_match_idx, "stage_weight"] = np.maximum(matches.loc[final_match_idx, "stage_weight"], 0.85)

print(f"Decider / Knockout matches flagged: {(matches['stage_weight'] >= 0.85).sum()} of {len(matches)}")

# --- 3. Merging Context into Deliveries ---
print("\n--- Enriching Deliveries with Context ---")
match_cols = [
    "match_id", "comp_id", "stage", "stage_weight", "home_team_id", "home_team",
    "away_team_id", "away_team", "knock_out", "revised_target", "is_series_decider",
    "win_team_id", "result"
]
bbb = bbb.merge(matches[match_cols], on="match_id", how="inner")
bbb = bbb.merge(comps[["comp_id", "comp_name", "match_format", "season"]], on="comp_id", how="left")

# Add team names
bbb["batting_team_name"] = bbb["batting_team_id"].map(team_dict).fillna("Unknown")
bbb["bowling_team_name"] = bbb["bowling_team_id"].map(team_dict).fillna("Unknown")

# Opponent team ranks
bbb["bowler_team_rank"] = bbb["bowling_team_name"].map(team_rank_map).fillna(DEFAULT_RANK)
bbb["batter_team_rank"] = bbb["batting_team_name"].map(team_rank_map).fillna(DEFAULT_RANK)

# --- 4. Delivery-Level Cricket Logic ---
print("Computing cricket delivery classifications...")
bbb["is_wide"] = bbb["extras_type"] == "wide"
bbb["is_noball"] = bbb["extras_type"] == "Overstep"
bbb["is_legal_bowler_ball"] = ~bbb["is_wide"] & ~bbb["is_noball"]
bbb["is_batter_ball_faced"] = ~bbb["is_wide"]

# Extra runs calculation
bbb["wide_runs"] = np.where(bbb["is_wide"], 1 + bbb["extras_2_runs"], 0)
bbb["noball_runs"] = np.where(bbb["is_noball"], 1 + bbb["extras_2_runs"], 0)
bbb["bye_legbye_runs"] = np.where(bbb["extras_type"].isin(["byes", "legbyes"]), 1 + bbb["extras_2_runs"], 0)

# Total runs on ball
bbb["delivery_total_runs"] = bbb["runs"] + bbb["wide_runs"] + bbb["noball_runs"] + bbb["bye_legbye_runs"]

# Bowler runs conceded (byes and legbyes are NOT charged to bowler)
bbb["bowler_runs_conceded"] = bbb["runs"] + bbb["wide_runs"] + bbb["noball_runs"]

# Bowler credited wickets
bowler_dismissals = ["Caught", "Bowled", "LBW", "Stump", "Hit Wicket"]
bbb["is_bowler_wicket"] = bbb["is_wicket"] & bbb["dismissal_type"].isin(bowler_dismissals)

# Boundaries and strike rotation
bbb["is_boundary"] = bbb["is_four"] | bbb["is_six"]
bbb["is_strike_rotation"] = (bbb["runs"].isin([1, 2, 3])) & (~bbb["is_boundary"])
bbb["is_dot_ball"] = (bbb["delivery_total_runs"] == 0) & (~bbb["is_wide"])

# --- 5. Chronological State Reconstruction ---
print("Reconstructing cumulative match states (runs, wickets, balls left, RRR)...")
bbb.sort_values(by=["match_id", "innings", "overid", "over_ball_num", "innings_ball_num"], inplace=True)

# Cumulative states per innings
bbb["cum_runs_before"] = bbb.groupby(["match_id", "innings"])["delivery_total_runs"].cumsum() - bbb["delivery_total_runs"]
bbb["cum_runs_after"] = bbb.groupby(["match_id", "innings"])["delivery_total_runs"].cumsum()

bbb["cum_wickets_before"] = bbb.groupby(["match_id", "innings"])["is_wicket"].cumsum() - bbb["is_wicket"].astype(int)
bbb["cum_wickets_after"] = bbb.groupby(["match_id", "innings"])["is_wicket"].cumsum()

bbb["cum_legal_balls"] = bbb.groupby(["match_id", "innings"])["is_legal_bowler_ball"].cumsum()
bbb["balls_left_innings"] = np.maximum(0, 120 - bbb["cum_legal_balls"])

# Current Run Rate (CRR)
bbb["crr"] = np.where(
    bbb["cum_legal_balls"] > 0,
    (bbb["cum_runs_after"] / bbb["cum_legal_balls"]) * 6.0,
    0.0
)

# Target computation for 2nd innings
# Find total 1st innings score per match
first_inn_totals = bbb[bbb["innings"] == 1].groupby("match_id")["delivery_total_runs"].sum()
bbb["target"] = np.nan
# Assign revised_target if present, else 1st inn total + 1
bbb.loc[bbb["innings"] == 2, "target"] = bbb.loc[bbb["innings"] == 2, "match_id"].map(first_inn_totals) + 1
bbb.loc[(bbb["innings"] == 2) & (bbb["revised_target"].notna()), "target"] = bbb.loc[
    (bbb["innings"] == 2) & (bbb["revised_target"].notna()), "revised_target"
]

# Runs required and Required Run Rate (RRR)
bbb["runs_required"] = np.where(
    bbb["innings"] == 2,
    np.maximum(0, bbb["target"] - bbb["cum_runs_before"]),
    np.nan
)
bbb["rrr"] = np.where(
    (bbb["innings"] == 2) & (bbb["balls_left_innings"] > 0),
    (bbb["runs_required"] / bbb["balls_left_innings"]) * 6.0,
    np.nan
)

# --- 6. Bowler Micro-Pressure: Conceded Boundary on Previous Ball ---
print("Flagging bowler post-boundary micro-pressure deliveries...")
bbb["prev_bowler_id"] = bbb.groupby(["match_id", "innings"])["bowler_id"].shift(1)
bbb["prev_is_boundary"] = bbb.groupby(["match_id", "innings"])["is_boundary"].shift(1).fillna(False)
bbb["bowler_post_boundary"] = (bbb["prev_bowler_id"] == bbb["bowler_id"]) & (bbb["prev_is_boundary"])

# Innings Phase Flags
bbb["phase"] = "Middle"
bbb.loc[bbb["overid"] <= 6, "phase"] = "Powerplay"
bbb.loc[bbb["overid"] >= 16, "phase"] = "Death"

# --- 7. Save Enriched Dataset ---
print(f"\n--- Saving Enriched Dataset to Parquet: {OUTPUT_PARQUET} ---")
bbb.to_parquet(OUTPUT_PARQUET, index=False)

summary_stats = {
    "total_deliveries": int(len(bbb)),
    "unique_matches": int(bbb["match_id"].nunique()),
    "unique_batters": int(bbb["striker_id"].nunique()),
    "unique_bowlers": int(bbb["bowler_id"].nunique()),
    "post_boundary_balls": int(bbb["bowler_post_boundary"].sum()),
    "knockout_or_decider_balls": int((bbb["stage_weight"] >= 0.85).sum()),
    "death_overs_balls": int((bbb["phase"] == "Death").sum()),
    "dot_balls": int(bbb["is_dot_ball"].sum()),
    "strike_rotation_balls": int(bbb["is_strike_rotation"].sum())
}

import json
with open(OUTPUT_SUMMARY, "w") as f:
    json.dump(summary_stats, f, indent=2)

print("Ingestion & Enrichment completed successfully!")
for k, v in summary_stats.items():
    print(f"  {k}: {v:,}")
