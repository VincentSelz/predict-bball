"""Assists by managing the Data."""
import pandas as pd

from bld.project_paths import project_paths_join as ppj


def abbrev_teams(dataset):
    """Replacing a list of teams with their abbrevations.

    Args: dataset

    Note: NBA teams change names semi-regularly - the function only accounts for the teams
    that changed names in the last 10 years.

    Out: Dataset with abbrevations
    """
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


def clean_base_function(year):
    """Get season data and do some basic cleaning and tidying.

        Args: year

        Notes: Reads in a excel file, then drops unnecessary columns and renames the headers.
        Adds two columns. Gets datetimes and names index and let index start at 1.

        Out: cleaned dataset
        """
    # List of column names(A, B, C are used to easier identify unnecessary columns)
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

    try:
        dc = pd.read_excel(ppj("IN_DATA", f"Boxscores{year}.xlsx"))
    except Exception:
        raise ValueError("The dataset for the specified year cannot be found.")

    # List of new columns names/ drop unncessary columns
    dc.columns = headers
    dc.drop(["A", "B", "C", "D", "E", "F"], axis=1, inplace=True)

    # Identifies Playoffs start and drops rows after that
    row = dc[dc.Date == "Playoffs"].index.tolist()[0]
    dc = dc.iloc[:row]

    # Converts date into useable dates
    dc.Date = pd.to_datetime(dc.Date)

    # Change team names to abbrevations
    abbrev_teams(dc)

    # Calculate Win Difference + Win Indicator
    dc["Win Difference"] = dc["PTS Home"].subtract(dc["PTS Away"])
    dc["Home Win"] = dc["Win Difference"].apply(lambda x: 1 if x >= 0 else 0)

    # Set index to 1
    dc.index = dc.index + 1
    dc.index.name = "gameid"

    return dc
