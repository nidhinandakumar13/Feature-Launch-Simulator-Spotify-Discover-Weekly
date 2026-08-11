"""
analyze.py
Analyzes the synthetic Spotify Discover Weekly dataset to test the hypothesis:
"Users who engage more with Discover Weekly (3+ songs/week) show higher
retention than users who don't."

Reads: data/spotify_dw_simulation.csv (or same-folder CSV if running in Colab)
Outputs: printed summary tables + a CSV ready for Tableau
"""

import pandas as pd

# ---- LOAD DATA ----
# If running in Colab and you saved the CSV in the main folder instead of
# a 'data' subfolder, change this path to just "spotify_dw_simulation.csv"
df = pd.read_csv("data/spotify_dw_simulation.csv")

print(f"Loaded {len(df)} rows, {df['user_id'].nunique()} unique users\n")

# ---- STEP 1: Define engagement flag ----
# "Engaged" = played 3+ Discover Weekly songs that week (our hypothesis threshold)
df["dw_engaged"] = df["dw_songs_played"] >= 3

# ---- STEP 2: Retention analysis ----
# For each user-week, figure out if they were active in the FOLLOWING week
df = df.sort_values(["user_id", "week"])
df["active_next_week"] = df.groupby("user_id")["weekly_active"].shift(-1)

# Only look at weeks where we know the following week's outcome (drop last week per user)
retention_df = df.dropna(subset=["active_next_week"])

# IMPORTANT: only compare users who were ACTIVE that week.
# Otherwise already-churned users (who always show dw_songs_played=0) get
# lumped into the "not engaged" group and drag its retention rate way down,
# exaggerating the apparent effect of DW engagement.
retention_df = retention_df[retention_df["weekly_active"] == 1]

retention_by_engagement = retention_df.groupby("dw_engaged")["active_next_week"].mean()

print("=== RETENTION: Next-week active rate ===")
print(f"Users who engaged with DW (3+ songs):     {retention_by_engagement[True]:.1%}")
print(f"Users who did NOT engage with DW:          {retention_by_engagement[False]:.1%}")
print(f"Retention lift from DW engagement:         {(retention_by_engagement[True] - retention_by_engagement[False]):.1%} points\n")

# ---- STEP 3: Weekly stickiness (like a simplified DAU/MAU) ----
weekly_active_rate = df.groupby("week")["weekly_active"].mean()
print("=== WEEKLY ACTIVE RATE (all users) ===")
print(weekly_active_rate.round(3), "\n")

# ---- STEP 4: Funnel ----
total_users = df["user_id"].nunique()
played_any_dw = df[df["dw_songs_played"] > 0]["user_id"].nunique()
played_3plus = df[df["dw_songs_played"] >= 3]["user_id"].nunique()
saved_any = df[df["dw_songs_saved"] > 0]["user_id"].nunique()

print("=== FUNNEL (users reaching each stage, at least once) ===")
print(f"Total users:                {total_users}")
print(f"Played 1+ DW song:          {played_any_dw}  ({played_any_dw/total_users:.1%})")
print(f"Played 3+ DW songs:         {played_3plus}  ({played_3plus/total_users:.1%})")
print(f"Saved 1+ DW song:           {saved_any}  ({saved_any/total_users:.1%})\n")

# ---- STEP 5: Save summary for Tableau ----
# Weekly retention rate split by engagement, per week (good for a line chart)
tableau_export = retention_df.groupby(["week", "dw_engaged"])["active_next_week"].mean().reset_index()
tableau_export.columns = ["week", "dw_engaged", "next_week_retention_rate"]
tableau_export.to_csv("data/retention_by_week_for_tableau.csv", index=False)

print("Saved 'data/retention_by_week_for_tableau.csv' for your Tableau dashboard.")
