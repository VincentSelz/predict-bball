"""This program scrapes basketball-reference.com to attain the scores
for each game in the specified season and exports them as excel files.
"""
# import time
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

# import requests

# NBA season that are analyzed
years = [2010, 2011, 2013, 2014, 2015, 2016, 2017, 2018, 2019]


def schedule_scraper(years):
    """
    This function takes a list of years as argument and scrapes the site for these years and
    returns the NBA schedule as Excel-document.
    Args: list of years
    """
    months = [
        "october",
        "november",
        "december",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
    ]

    box_scores = {}
    for year in years:
        box_scores[year] = []
        for month in months:
            try:
                url = (
                    f"https://www.basketball-reference.com/"
                    "leagues/NBA_{year}_games-{month}.html"
                )
                # Is the URL accessible?
                # response = requests.get(url)
                # this is the HTML from the given URL
                html = urlopen(url)
                soup = BeautifulSoup(html)
            except HTTPError as err:
                if err.code == 404:
                    continue
                else:
                    raise HTTPError  # TODO: FInd better Error + Message
            # use findALL() to get the column headers
            soup.findAll("tr", limit=2)

            # use getText()to extract the text we need into a list
            headers = [
                th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")
            ]

            # avoid the first header row
            rows = soup.findAll("tr")[1:]
            games = [[td.getText() for td in rows[i]] for i in range(len(rows))]

            # Convert into Dataframe
            month = pd.DataFrame(games, columns=headers)
            box_scores[year].append(month)

        # Create a Dataframe for each year
        box_scores[year] = pd.concat(box_scores[year])

        # Export it as Excel file
        # box_scores[year].to_excel("../Data/Boxscores"+ str(year) +".xlsx")
