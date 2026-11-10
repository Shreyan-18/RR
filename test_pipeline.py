import os
import pandas as pd
import numpy as np

data_dir = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"

print("Loading datasets...")
comps = pd.read_csv(os.path.join(data_dir, "competitions.csv"))
matches = pd.read_csv(os.path.join(data_dir, "matches.csv"))
teams = pd.read_csv(os.path.join(data_dir, "teams.csv"))
mapping = pd.read_csv(os.path.join(data_dir, "competition_team_player_mapping.csv"))
bbb = pd.read_csv(os.path.join(data_dir, "ball_by_ball.csv"))

print(f"Loaded: comps={len(comps)}, matches={len(matches)}, bbb={len(bbb)}")

# 1. Define Team Strength / Ranks
team_rank_map = {
    # Tier 1 (Rank 1.0)
    "India": 1.0,
    # Tier 2 (Rank 1.25)
    "England": 1.25, "Australia": 1.25, "South Africa": 1.25, "New Zealand": 1.25,
    # Tier 3 (Rank 1.5)
    "Pakistan": 1.5, "West Indies": 1.5, "Sri Lanka": 1.5, "Afghanistan": 1.5,
    # Tier 4 (Rank 1.8)
    "Bangladesh": 1.8, "Ireland": 1.8, "Zimbabwe": 1.8, "Netherlands": 1.8, 
    "Scotland": 1.8, "United States Of America": 1.8,
    # IPL teams (Treated as Tier 1.5 equivalent elite club competition)
    "Chennai Super Kings": 1.3, "Mumbai Indians": 1.3, "Gujarat Titans": 1.35,
    "Kolkata Knight Riders": 1.35, "Rajasthan Royals": 1.35, "Sunrisers Hyderabad": 1.4,
    "Royal Challengers Bengaluru": 1.4, "Delhi Capitals": 1.45, "Lucknow Super Giants": 1.45,
    "Punjab Kings": 1.5
}
# Default for other Associate / A teams
default_rank = 2.0

# 2. Identify Match Stakes (Knockout vs Must-Win vs Regular)
# Check stages
stage_stakes = {
    "Final": 1.0,
    "Semi Final": 0.95,
    "Eliminator": 0.95,
    "Qualifier": 0.90,
    "Super 4": 0.80,
    "League": 0.50,
    "Others": 0.50
}
matches["stage_weight"] = matches["stage"].map(stage_stakes).fillna(0.50)
matches.loc[matches["knock_out"] == 1, "stage_weight"] = np.maximum(matches["stage_weight"], 0.90)

# Merge match metadata into BBB
bbb = bbb.merge(
    matches[["match_id", "comp_id", "stage", "stage_weight", "home_team", "away_team", "knock_out", "revised_target"]],
    on="match_id",
    how="left"
)

# Merge comp info
bbb = bbb.merge(comps[["comp_id", "comp_name", "match_format"]], on="comp_id", how="left")

# Assign bowling team name and opponent quality weight
teams_dict = teams.drop_duplicates(subset=["team_id"]).set_index("team_id")["team_name"].to_dict()
bbb["batting_team_name"] = bbb["batting_team_id"].map(teams_dict)
bbb["bowling_team_name"] = bbb["bowling_team_id"].map(teams_dict)

# Opponent rank for batter (bowling team quality)
bbb["bowler_team_rank"] = bbb["bowling_team_name"].map(team_rank_map).fillna(default_rank)
# Opponent rank for bowler (batting team quality)
bbb["batter_team_rank"] = bbb["batting_team_name"].map(team_rank_map).fillna(default_rank)

# 3. Post-Boundary Micro-Pressure for Bowlers
# Sort chronologically by match, innings, overid, over_ball_num
bbb.sort_values(by=["match_id", "innings", "overid", "over_ball_num"], inplace=True)
bbb["is_boundary"] = bbb["is_four"] | bbb["is_six"]

# Bowler's previous ball in the same match
bbb["prev_bowler_id"] = bbb.groupby(["match_id", "innings"])["bowler_id"].shift(1)
bbb["prev_is_boundary"] = bbb.groupby(["match_id", "innings"])["is_boundary"].shift(1).fillna(False)
bbb["bowler_post_boundary"] = (bbb["prev_bowler_id"] == bbb["bowler_id"]) & (bbb["prev_is_boundary"])

print("Bowler post-boundary balls:", bbb["bowler_post_boundary"].sum())
print("Test completed successfully!")
