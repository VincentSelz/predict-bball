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
    """
    This function takes a list of years as argument and scrapes the site for these years and
    returns the NBA schedules as Excel-document.

    Args: list of years

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
        # Export it as Excel file with Waf
        # box_scores[year].to_excel(ppj("OUT_DATA","Boxscores" + str(year) + ".xlsx"),sep="/")
        # Export it without waf
        box_scores[year].to_csv("../data/Boxscores" + str(year) + ".csv")
    return print("Exported all Boxscores successfully!")


schedule_scraper(years)
