"""This program scrapes basketball-reference.com to attain the scores
for each game in the specified season and exports them as excel files.
"""
# import time
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

# NBA season that are analyzed
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

box_scores = []
for month in months:
    try:
        url = f"""https://www.basketball-reference.com/leagues/NBA_2012_games-{month}.html"""

        # Is the URL accessible?
        response = requests.get(url)
        # this is the HTML from the given URL
        html = urlopen(url)
        soup = BeautifulSoup(html)
    except HTTPError as err:
        if err.code == 404:
            continue
        else:
            raise HTTPError
    # use findALL() to get the column headers
    soup.findAll("tr", limit=2)

    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]

    # avoid the first header row
    rows = soup.findAll("tr")[1:]
    games = [[td.getText() for td in rows[i]] for i in range(len(rows))]

    # Convert into Dataframe
    month = pd.DataFrame(games, columns=headers)
    box_scores.append(month)
box_scores = pd.concat(box_scores)
