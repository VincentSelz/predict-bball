"""This script reads in data cleans/curates it and does first steps toward analyzing it."""
import pandas as pd

# from bld.project_paths import project_paths_join as ppj
# Works for Waf
# dataset = pd.read_excel((ppj("OUT_DATA","Seasons.xlsx")))
dataset = pd.read_excel("../data/Seasons.xlsx")
# # TODO: specifiy what can be dropped and what not
clean_data = dataset.dropna()
clean_data = clean_data[
    [
        "gameid",
        "Date",
        "Away Team",
        "PTS Away",
        "Home Team",
        "PTS Home",
        "Win Difference",
        "Home Win",
        "Games No Home Team",
        "Games No Away Team",
        "Home Wins",
        "Away Wins",
        "Home Losses",
        "Away Losses",
        "Home PTS Average",
        "Away PTS Average",
        "Home OPP PTS Average",
        "Away OPP PTS Average",
        "Home Win Percentage",
        "Away Win Percentage",
        "Home Point Differential",
        "Away Point Differential",
        "Home Days Off",
        "Away Days Off",
    ]
]
array = clean_data.values
