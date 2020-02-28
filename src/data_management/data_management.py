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
dc["Win Difference"] = dc["PTS Home"].subtract(dc["PTS Away"])

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

# Create DataFrames for Away & Home teams of a certain team
Home_All = []
Away_All = []
Season = {}
Home = {}
Away = {}
for team in teams:
    Home[team] = dc[dc["Home Team"].str.match(f"{team}")]
    Away[team] = dc[dc["Away Team"].str.match(f"{team}")]
    Home[team][f"{team} Home"] = 1
    Away[team][f"{team} Home"] = 0

    # Get Wins
    Home[team][f"{team} Win"] = Home[team]["Home Win"]
    Away[team][f"{team} Win"] = Away[team]["Away Win"]
    Home[team][f"{team} Loss"] = Home[team]["Home Win"].apply(
        lambda x: 1 if x == 0 else 0
    )
    Away[team][f"{team} Loss"] = Away[team]["Away Win"].apply(
        lambda x: 1 if x == 0 else 0
    )
    Home[team][f"{team} PTS"] = Home[team]["PTS Home"]
    Away[team][f"{team} PTS"] = Away[team]["PTS Away"]
    Home[team][f"OPP PTS"] = Home[team]["PTS Away"]
    Away[team][f"OPP PTS"] = Away[team]["PTS Home"]

    # Concat the Dataframes
    Season[team] = pd.concat([Home[team], Away[team]])

    # Sort by index /very important since we predict on past games
    Season[team].sort_index(inplace=True)

    # set gameid as index and put games as column
    games = [*range(1, len(Season[team]) + 1)]
    Season[team]["games"] = games
    Season[team].reset_index(inplace=True)
    Season[team].set_index(["gameid"], inplace=True)

    # Cumulative Wins/Losses + Average Points
    Season[team]["Wins"] = Season[team][f"{team} Win"].cumsum().shift(+1)
    Season[team]["Losses"] = Season[team][f"{team} Loss"].cumsum().shift(+1)
    Season[team][f"{team} PTS Average"] = (
        Season[team][f"{team} PTS"].cumsum().divide(Season[team]["games"]).shift(+1)
    )
    Season[team]["OPP PTS Average"] = (
        Season[team]["OPP PTS"].cumsum().divide(Season[team]["games"]).shift(+1)
    )

    # Clean the Dataframe
    Season[team].drop(
        columns=[
            "Away Win",
            f"{team} Home",
            f"{team} Win",
            f"{team} Loss",
            f"{team} PTS",
            "OPP PTS",
            "games",
        ],
        inplace=True,
    )

    # Putting it into form to get it back into the original Dataframe
    Home[team] = Season[team][Season[team]["Home Team"].str.match(f"{team}")]
    Away[team] = Season[team][Season[team]["Away Team"].str.match(f"{team}")]
    # Home[team].drop(columns=["Away Team","Home Team"],inplace=True)
    Away[team].drop(
        columns=[
            "Away Team",
            "Home Team",
            "Date",
            "PTS Away",
            "PTS Home",
            "Win Difference",
            "Home Win",
        ],
        inplace=True,
    )
    # Rename Indicators
    Home[team].rename(
        columns={
            f"{team} PTS Average": "Home PTS Average",
            "OPP PTS Average": "Home OPP PTS Average",
            "Wins": "Home Wins",
            "Losses": "Home Losses",
        },
        inplace=True,
    )
    Away[team].rename(
        columns={
            f"{team} PTS Average": "Away PTS Average",
            "OPP PTS Average": "Away OPP PTS Average",
            "Wins": "Away Wins",
            "Losses": "Away Losses",
        },
        inplace=True,
    )

    # TODO
    # seas = dc.merge(Home[team],how='left',left_index=True, right_index=True)
    # seas = dc.merge(Away[team],how='left', left_index=True, right_index=True)
    Home_All.append(Home[team])
    Away_All.append(Away[team])
    # season_data = pd.concat([season_data, Home[team]], sort=False)
    # season_data = pd.concat([season_data, Away[team]], sort=False)
Home_All = pd.concat(Home_All)
Away_All = pd.concat(Away_All)
Season_data = Home_All.join(Away_All)
Season_data.sort_index(inplace=True)
Season_data.to_excel("Season2018_data.xlsx")
