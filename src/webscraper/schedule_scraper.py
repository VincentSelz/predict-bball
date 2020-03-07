"""Scrapes basketball-reference.com to attain the scores
for each game in the specified season and exports them as excel files.
"""
import time

import pandas as pd
from helper_functions import fetch_games
from helper_functions import get_URLs


# NBA season that are analyzed
years = list(range(2010, 2020))


def schedule_scraper(years):
    """Scrapes schedule and spits them out as Excel files.""

    Arg: list of years

    Functionality: This function parses through each specified year and stores the data
    in a Dictionary with years as keys. Next, these Dataframe are exported as an Excel file.

    """
    box_scores = {}
    for year in years:
        urls = get_URLs(year)
        box_scores[year] = []
        for url in urls:
            try:  # CLean this mess up ASAP
                month = fetch_games(url)
            except Exception:
                continue
            box_scores[year].append(month)
            # As specified in the robots.txt of the website.
            time.sleep(3)
        # Create a Dataframe for each year
        box_scores[year] = pd.concat(box_scores[year])
        # Export it as Excel file
        box_scores[year].to_excel("../data/Boxscores" + str(year) + ".xlsx")
    return print("Exported all Boxscores successfully!")


schedule_scraper(years)
