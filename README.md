# Feature Launch Simulator: Spotify Discover Weekly

A simulated data analysis project evaluating whether Spotify's Discover Weekly feature drives user retention — built to practice the kind of analysis a product manager would run after a feature launch.

## The idea

Discover Weekly is a personalized playlist Spotify refreshes every Monday. The hypothesis: users who actually engage with it (listen to 3+ songs from it in a week) should be more likely to stay active the following week than users who ignore it.

## What I did

1. **Generated synthetic data** — simulated 2,000 users over 12 weeks in Python (Pandas, NumPy), including how many Discover Weekly songs each user played, saved, and whether they stayed active week to week.
2. **Analyzed retention** — compared next-week retention rates between engaged and non-engaged users.
3. **Caught a bug** — my first pass showed an unrealistically huge gap. Turned out churned users (who obviously play 0 DW songs) were getting lumped into the "not engaged" group, dragging that number down artificially. Fixed it by only comparing users who were active that week.
4. **Built a dashboard** — visualized the corrected retention trend in Tableau.

## Key finding

Users who engaged with Discover Weekly (3+ songs/week) had an **85.5% retention rate** the following week, compared to **48%** for users who didn't engage — a real, meaningful lift even after correcting for the bug above.

## Files

- `generate_data.py` — builds the synthetic dataset
- `analyze.py` — calculates retention, funnel, and stickiness metrics
- [Tableau Dashboard](#) — interactive view of the retention trend *(replace this with your actual Tableau Public link)*

## Tools used

Python, Pandas, NumPy, Tableau Public
