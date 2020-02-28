"""This file reads in all the scraped Excel file and than manipulates them in
a way to attain one Dataframe with all games.
"""
import pandas as pd

dc = pd.read_excel("../data/Boxscores2018.xlsx")

# List of new columns names
list = [
    "A",
    "Date",
    "B",
    "Away Team",
    "PTS Away",
    "Home Team",
    "PTS Home",
    "C",
    "D",
    "E",
    "F",
]
dc.columns = list

# Drop Columns
dc.drop(["A", "B", "C", "D", "E", "F"], axis=1, inplace=True)

# Identifies Playoffs start and drops rows after that
row = dc[dc["Date"] == "Playoffs"].index.tolist()[0]
dc = dc.iloc[:row]

# Get win/loss amount of home team
dc["Win Difference"] = dc["PTS Home"].subtract(dc["PTS Away"])  # is a series
# dc = pd.concat([df, diff], axis=1) #This has to before the index is reset
# dc.rename(columns={0: "Win Difference"}, inplace=True)

# Win Indicator
dc["Home Win"] = dc["Win Difference"].apply(lambda x: 1 if x >= 0 else 0)
dc["Away Win"] = dc["Win Difference"].apply(lambda x: 1 if x <= 0 else 0)

# Change Team Names
dc.replace(
    {
        "Cleveland Cavaliers": "CLE",
        "Golden State Warriors": "GSW",
        "Detroit Pistons": "DET",
        "Indiana Pacers": "IND",
        "Orlando Magic": "ORL",
        "Washington Wizards": "WAS",
        "Boston Celtics": "BOS",
        "Memphis Grizzlies": "MEM",
        "Dallas Mavericks": "DAL",
        "Utah Jazz": "UTA",
        "San Antonio Spurs": "SAS",
        "Phoenix Suns": "PHX",
        "Sacramento Kings": "SAC",
        "Toronto Raptors": "TOR",
        "Oklahoma City Thunder": "OKC",
        "Los Angeles Lakers": "LAL",
        "Charlotte Hornets": "CHA",
        "Milwaukee Bucks": "MIL",
        "Philadelphia 76ers": "PHI",
        "Brooklyn Nets": "BKN",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "Chicago Bulls": "CHI",
        "Houston Rockets": "HOU",
        "Miami Heat": "MIA",
        "New York Knicks": "NYK",
        "Denver Nuggets": "DEN",
        "Los Angeles Clippers": "LAC",
        "Portland Trail Blazers": "POR",
        "Atlanta Hawks": "ATL",
        "New Orleans Hornets": "NOH",
        "Charlotte Bobcats": "CHB",
    },
    inplace=True,
)

# Set index to 1
dc.index = dc.index + 1
dc.index.name = "gameid"
season_data = dc
# List of teams
teams = dc["Home Team"].unique().tolist()
