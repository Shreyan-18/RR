"""
SupeRR Selector Season 2 - Psychological & Form Layer:
Calculates:
1. Bowler Post-Wicket Momentum:
   - Bowler takes a wicket on previous delivery -> Bowler confidence surge (-0.15 pressure on bowler),
     incoming batter crisis/cold-start (+0.15 pressure on batter).
2. Batter In-Game Flow State:
   - Cold/New batter (balls faced < 8) -> Vulnerability zone (+0.12 pressure).
   - Set batter (balls faced >= 18, runs >= 20) -> In flow state (-0.10 pressure relief).
   - Batter post-boundary -> Momentum upper hand (-0.08 pressure relief).
   - Dot ball buildup -> 3+ consecutive dots faced by batter (+0.10 pressure).
3. Pre-Match Rolling Form (Last 3 Matches):
   - Batter in slump (last 3 matches: < 30 runs with >= 20 balls) -> Self-doubt (+0.10 pressure).
   - Batter in peak form (last 3 matches: >= 90 runs, SR >= 135) -> Freedom/Confidence (-0.08 pressure relief).
   - Bowler in slump (last 3 matches: 0 wickets, econ > 9.5) -> Pressure to defend place (+0.10 pressure).
   - Bowler in peak form (last 3 matches: >= 5 wickets, econ < 7.5) -> High rhythm (-0.08 pressure relief).
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\prana\.gemini\antigravity\scratch\superr_selector"
PARQUET_PATH = os.path.join(DATA_DIR, "enriched_ball_by_ball.parquet")

print("--- Adding Psychological & Form Dynamics to Deliveries ---")
df = pd.read_parquet(PARQUET_PATH)
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))

# Ensure chronological ordering
matches["match_date"] = pd.to_datetime(matches["match_date"])
match_dates = matches.set_index("match_id")["match_date"].to_dict()
df["match_date"] = df["match_id"].map(match_dates)

df.sort_values(by=["match_date", "match_id", "innings", "overid", "over_ball_num", "innings_ball_num"], inplace=True)

# ==========================================
# 1. BOWLER POST-WICKET MOMENTUM & TARGET
# ==========================================
print("1. Computing Bowler Post-Wicket Momentum...")
df["prev_bowler_id"] = df.groupby(["match_id", "innings"])["bowler_id"].shift(1)
df["prev_is_wicket"] = df.groupby(["match_id", "innings"])["is_bowler_wicket"].shift(1).fillna(False)

# Bowler delivered a wicket on the immediate previous ball
df["bowler_post_wicket"] = (df["prev_bowler_id"] == df["bowler_id"]) & df["prev_is_wicket"]
print(f"  Deliveries immediately following a bowler wicket: {df['bowler_post_wicket'].sum():,}")

# ==========================================
# 2. BATTER IN-GAME FLOW STATE
# ==========================================
print("2. Computing Batter In-Game Flow State...")
# Cumulative balls faced and runs scored in current innings before this ball
df["batter_innings_balls"] = df.groupby(["match_id", "innings", "striker_id"])["is_batter_ball_faced"].cumsum() - df["is_batter_ball_faced"].astype(int)
df["batter_innings_runs"] = df.groupby(["match_id", "innings", "striker_id"])["runs"].cumsum() - df["runs"]

# Cold vs Set batter
df["batter_is_cold"] = df["batter_innings_balls"] < 8
df["batter_is_set"] = (df["batter_innings_balls"] >= 18) & (df["batter_innings_runs"] >= 20)

# Batter previous ball outcome (for batter confidence)
df["batter_prev_runs"] = df.groupby(["match_id", "innings", "striker_id"])["runs"].shift(1)
df["batter_post_boundary"] = df["batter_prev_runs"].isin([4, 6])

# Consecutive dots faced by batter
is_dot = (df["runs"] == 0) & (~df["is_wide"])
df["dot_streak"] = 0
# Track dot streak within innings for each striker
def get_dot_streaks(series):
    streaks = []
    curr = 0
    for val in series:
        streaks.append(curr)
        if val:
            curr += 1
        else:
            curr = 0
    return streaks

# Vectorized dot streak per batter in innings
df["is_dot_faced"] = is_dot & df["is_batter_ball_faced"]
df["prev_dot"] = df.groupby(["match_id", "innings", "striker_id"])["is_dot_faced"].shift(1).fillna(False)
df["dot_pressure_building"] = df.groupby(["match_id", "innings", "striker_id"])["prev_dot"].transform(
    lambda s: s.rolling(3, min_periods=3).sum() == 3
).fillna(False)

print(f"  Cold / New batter deliveries: {df['batter_is_cold'].sum():,}")
print(f"  Set batter deliveries: {df['batter_is_set'].sum():,}")
print(f"  Deliveries right after batter hit a boundary: {df['batter_post_boundary'].sum():,}")

# ==========================================
# 3. PRE-MATCH ROLLING FORM (LAST 3 MATCHES)
# ==========================================
print("3. Computing Pre-Match Rolling Form for Batters and Bowlers...")

# A. Batter Match History
batter_match_stats = df.groupby(["striker_id", "match_id", "match_date"]).agg(
    match_runs=("runs", "sum"),
    match_balls=("is_batter_ball_faced", "sum"),
    dismissed=("is_wicket", "sum")
).reset_index()
batter_match_stats.sort_values(by=["striker_id", "match_date", "match_id"], inplace=True)

# Rolling 3 matches prior to current match (shift 1 ensures current match is NOT leaked!)
batter_match_stats["rolling_runs_last3"] = batter_match_stats.groupby("striker_id")["match_runs"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=1).sum()
).fillna(0)
batter_match_stats["rolling_balls_last3"] = batter_match_stats.groupby("striker_id")["match_balls"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=1).sum()
).fillna(0)

batter_match_stats["batter_in_slump"] = (batter_match_stats["rolling_runs_last3"] < 30) & (batter_match_stats["rolling_balls_last3"] >= 20)
batter_match_stats["batter_in_form"] = (batter_match_stats["rolling_runs_last3"] >= 90) & (
    (batter_match_stats["rolling_runs_last3"] / np.maximum(1, batter_match_stats["rolling_balls_last3"])) * 100 >= 135
)

# Merge back to deliveries
df = df.merge(
    batter_match_stats[["striker_id", "match_id", "rolling_runs_last3", "batter_in_slump", "batter_in_form"]],
    on=["striker_id", "match_id"],
    how="left"
)
df["batter_in_slump"] = df["batter_in_slump"].fillna(False)
df["batter_in_form"] = df["batter_in_form"].fillna(False)

# B. Bowler Match History
bowler_match_stats = df.groupby(["bowler_id", "match_id", "match_date"]).agg(
    match_wkts=("is_bowler_wicket", "sum"),
    match_runs_conceded=("bowler_runs_conceded", "sum"),
    match_balls=("is_legal_bowler_ball", "sum")
).reset_index()
bowler_match_stats.sort_values(by=["bowler_id", "match_date", "match_id"], inplace=True)

# Rolling 3 matches prior
bowler_match_stats["rolling_wkts_last3"] = bowler_match_stats.groupby("bowler_id")["match_wkts"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=1).sum()
).fillna(0)
bowler_match_stats["rolling_runs_last3"] = bowler_match_stats.groupby("bowler_id")["match_runs_conceded"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=1).sum()
).fillna(0)
bowler_match_stats["rolling_balls_last3"] = bowler_match_stats.groupby("bowler_id")["match_balls"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=1).sum()
).fillna(0)

bowler_match_stats["rolling_econ_last3"] = np.where(
    bowler_match_stats["rolling_balls_last3"] > 0,
    (bowler_match_stats["rolling_runs_last3"] / bowler_match_stats["rolling_balls_last3"]) * 6.0,
    7.5
)

bowler_match_stats["bowler_in_slump"] = (bowler_match_stats["rolling_wkts_last3"] == 0) & (bowler_match_stats["rolling_econ_last3"] >= 9.5) & (bowler_match_stats["rolling_balls_last3"] >= 36)
bowler_match_stats["bowler_in_form"] = (bowler_match_stats["rolling_wkts_last3"] >= 5) & (bowler_match_stats["rolling_econ_last3"] <= 7.5)

# Merge back to deliveries
df = df.merge(
    bowler_match_stats[["bowler_id", "match_id", "rolling_wkts_last3", "bowler_in_slump", "bowler_in_form"]],
    on=["bowler_id", "match_id"],
    how="left"
)
df["bowler_in_slump"] = df["bowler_in_slump"].fillna(False)
df["bowler_in_form"] = df["bowler_in_form"].fillna(False)

print(f"  Batters facing delivery while in recent slump: {df['batter_in_slump'].sum():,}")
print(f"  Batters facing delivery while in peak form: {df['batter_in_form'].sum():,}")
print(f"  Bowlers delivering while in recent slump: {df['bowler_in_slump'].sum():,}")
print(f"  Bowlers delivering while in peak form: {df['bowler_in_form'].sum():,}")

# Clean temporary columns
temp_cols = ["prev_is_wicket", "prev_bowler_id", "prev_dot", "is_dot_faced"]
df.drop(columns=[c for c in temp_cols if c in df.columns], inplace=True)

# Save enriched parquet
print(f"\nSaving updated enriched deliveries with Psychological & Form Layer to {PARQUET_PATH}...")
df.to_parquet(PARQUET_PATH, index=False)
print("Psychological & Form dynamics successfully incorporated!")
