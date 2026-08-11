"""
generate_data.py
Generates synthetic Spotify user engagement data to simulate the impact
of Discover Weekly (DW) on user retention.

Output: data/spotify_dw_simulation.csv
One row per user per week (long format), across 12 weeks.
"""

import numpy as np
import pandas as pd
import os

# ---- CONFIG ----
NUM_USERS = 2000
NUM_WEEKS = 12
OUTPUT_PATH = "data/spotify_dw_simulation.csv"

np.random.seed(42)  # reproducible results

rows = []

for user_id in range(1, NUM_USERS + 1):
    # Each user has a "baseline" engagement level (some people are just more active)
    baseline_activity = np.random.beta(2, 2)  # skews toward mid-range activity

    # Some users are "DW responders" - they engage more with Discover Weekly
    # and this is baked in to have a real effect on retention (our hypothesis)
    is_dw_responder = np.random.rand() < 0.4  # 40% of users respond well to DW

    active_last_week = True  # everyone starts active in week 1

    for week in range(1, NUM_WEEKS + 1):

        # If they weren't active last week, most stay inactive (churned)
        if not active_last_week:
            weekly_active = np.random.rand() < 0.05  # small chance of winback
            dw_songs_played = 0
            dw_songs_saved = 0
            total_sessions = 0
        else:
            weekly_active = True

            # How many DW songs they play this week depends on responder type
            if is_dw_responder:
                dw_songs_played = np.random.poisson(lam=6)  # responders engage more
            else:
                dw_songs_played = np.random.poisson(lam=1.5)

            dw_songs_played = min(dw_songs_played, 30)  # cap at playlist size

            # Saves are a fraction of songs played
            dw_songs_saved = np.random.binomial(dw_songs_played, p=0.15)

            # Total sessions this week, influenced by baseline activity
            total_sessions = max(0, int(np.random.normal(
                loc=3 + baseline_activity * 4, scale=1.5)))

            # --- THE HYPOTHESIS, baked into the data ---
            # Users who played 3+ DW songs this week are MORE likely to be
            # active next week than users who didn't engage with DW.
            if dw_songs_played >= 3:
                retention_prob = 0.85
            else:
                retention_prob = 0.55

            active_last_week = np.random.rand() < retention_prob

        rows.append({
            "user_id": user_id,
            "week": week,
            "is_dw_responder": is_dw_responder,
            "weekly_active": int(weekly_active),
            "dw_songs_played": dw_songs_played,
            "dw_songs_saved": dw_songs_saved,
            "total_sessions": total_sessions,
        })

df = pd.DataFrame(rows)

os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Generated {len(df)} rows for {NUM_USERS} users over {NUM_WEEKS} weeks.")
print(f"Saved to {OUTPUT_PATH}")
print(df.head(10))
