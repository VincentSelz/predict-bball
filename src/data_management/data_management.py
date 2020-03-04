"""This file reads in all the scraped Excel file and than manipulates them in
a way to attain one Dataframe with all games.
"""
import pandas as pd

from bld.project_paths import project_paths_join as ppj

years = list(range(2010, 2020))


def abbrev_teams(dataset):
    dataset.replace(
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
            # Deprecated Teams
            "New Orleans Hornets": "NOH",
            "Charlotte Bobcats": "CHB",
            "New Jersey Nets": "NJN",
        },
        inplace=True,
    )


def save_data(sample):
    sample.to_csv(ppj("OUT_DATA", f"{sample}.csv"), sep=",")


# List of column names(A, B, C are used to easier indentifiy unnecessary columns)
headers = [
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

Seasons = []
for year in years:
    # dc = pd.read_excel(f"../data/Boxscores{year}.xlsx", parse_dates=True)
    # dc = pd.read_excel(f"Boxscores{year}.xlsx",parse_dates=True)
    # dc = pd.read_csv(f"../data/Boxscores{year}.csv", parse_dates=True)
    dc = pd.read_csv(ppj("DATA", f"Boxscores{year}.csv", parse_dates=True), sep=",")
    # List of new columns names
    dc.columns = headers

    # Drop Columns (some Colunms were unspecified)
    dc.drop(["A", "B", "C", "D", "E", "F"], axis=1, inplace=True)

    # Identifies Playoffs start and drops rows after that
    row = dc[dc.Date == "Playoffs"].index.tolist()[0]
    dc = dc.iloc[:row]

    # Converts date into useable dates
    dc.Date = pd.to_datetime(dc.Date)

    # Change team names to abbrevations
    abbrev_teams(dc)

    # Calculate Win Difference
    dc["Win Difference"] = dc["PTS Home"].subtract(dc["PTS Away"])

    # Win Indicator
    dc["Home Win"] = dc["Win Difference"].apply(lambda x: 1 if x >= 0 else 0)

    # Set index to 1
    dc.index = dc.index + 1
    dc.index.name = "gameid"

    # List of teams
    teams = dc["Home Team"].unique().tolist()

    # Create Dictionary of Dateframes for all teams
    Home_All = []
    Away_All = []
    Season = {}
    Home = {}
    Away = {}
    for team in teams:

        Home[team] = dc[dc["Home Team"].str.match(f"{team}")]
        Away[team] = dc[dc["Away Team"].str.match(f"{team}")]

        # Get Wins #Copy Warning
        Home[team][f"{team} Win"] = Home[team]["Home Win"]
        Away[team][f"{team} Win"] = Away[team]["Home Win"].apply(
            lambda x: 1 if x == 0 else 0
        )
        Home[team][f"{team} Loss"] = Home[team]["Home Win"].apply(
            lambda x: 1 if x == 0 else 0
        )
        Away[team][f"{team} Loss"] = Away[team]["Home Win"].apply(
            lambda x: 1 if x == 1 else 0
        )
        # Get points #Copy Warning
        Home[team][f"{team} PTS"] = Home[team]["PTS Home"]
        Away[team][f"{team} PTS"] = Away[team]["PTS Away"]
        Home[team][f"OPP PTS"] = Home[team]["PTS Away"]
        Away[team][f"OPP PTS"] = Away[team]["PTS Home"]

        # Concat the Dataframes
        Season[team] = pd.concat([Home[team], Away[team]])

        # Sort by index (very important since we predict on past games)
        Season[team].sort_index(inplace=True)

        # Put games as column
        Season[team]["Games"] = [*range(1, len(Season[team]) + 1)]

        # Cumulative Wins/Losses & Win Percentage
        Season[team]["Wins"] = Season[team][f"{team} Win"].cumsum().shift(+1)
        Season[team]["Losses"] = Season[team][f"{team} Loss"].cumsum().shift(+1)
        Season[team]["Win Percentage"] = Season[team]["Wins"].divide(
            Season[team]["Games"].shift(+1)
        )

        # Average Points & Point Differential
        Season[team][f"{team} PTS Average"] = (
            Season[team][f"{team} PTS"].cumsum().divide(Season[team]["Games"]).shift(+1)
        )
        Season[team]["OPP PTS Average"] = (
            Season[team]["OPP PTS"].cumsum().divide(Season[team]["Games"]).shift(+1)
        )
        Season[team]["Point Differential"] = Season[team][
            f"{team} PTS Average"
        ].subtract(Season[team]["OPP PTS Average"])

        # Days off
        Season[team]["Days Off"] = Season[team]["Date"].subtract(
            Season[team]["Date"].shift(+1)
        )

        # Clean the Dataframe
        Season[team].drop(
            columns=[f"{team} Win", f"{team} Loss", f"{team} PTS", "OPP PTS"],
            inplace=True,
        )

        # Putting it into form to get it back into the original Dataframe
        Home[team] = Season[team][Season[team]["Home Team"].str.match(f"{team}")]
        Away[team] = Season[team][Season[team]["Away Team"].str.match(f"{team}")]

        # Reduces complexity and makes later joint with other Dataframe easier.
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

        # Rename Indicators into general names
        Home[team].rename(
            columns={
                f"{team} PTS Average": "Home PTS Average",
                "OPP PTS Average": "Home OPP PTS Average",
                "Wins": "Home Wins",
                "Losses": "Home Losses",
                "Win Percentage": "Home Win Percentage",
                "Games": "Games No Home Team",
                "Point Differential": "Home Point Differential",
                "Days Off": "Home Days Off",
            },
            inplace=True,
        )
        Away[team].rename(
            columns={
                f"{team} PTS Average": "Away PTS Average",
                "OPP PTS Average": "Away OPP PTS Average",
                "Wins": "Away Wins",
                "Losses": "Away Losses",
                "Win Percentage": "Away Win Percentage",
                "Games": "Games No Away Team",
                "Point Differential": "Away Point Differential",
                "Days Off": "Away Days Off",
            },
            inplace=True,
        )

        # Append Data to list
        Home_All.append(Home[team])
        Away_All.append(Away[team])

    # List to Dataframe
    Home_All = pd.concat(Home_All)
    Away_All = pd.concat(Away_All)

    # Join the two lists together
    Season_data = Home_All.join(Away_All)
    Season_data.sort_index(inplace=True)

    # Export data per year as csv file
    Season_data.to_excel(ppj("DATA_MANAGEMENT", f"Season{year}_data.csv"), sep=",")

    # Get list of all season together
    Seasons.append(Season_data)

# List to Dataframe
Seasons = pd.concat(Seasons)
save_data(Seasons)
