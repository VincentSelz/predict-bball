"""Helper functions.
"""
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup


def get_URLs(year):
    """Stores URLs.

    Arg: year

    Functionality: Stores the working URL for a prespecified year in a list.

    Notes: Month include all months were the NBA is playing but there are instances,
    were the season begins later, thus the necessity to check the URLs.
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

    urls = []
    for month in months:
        url = (
            f"https://www.basketball-reference.com/"
            "leagues/NBA_{}_games-{}.html".format(year, month)
        )
        try:
            urlopen(url)
            urls.append(url)
        except HTTPError as err:
            if err.code == 404:
                continue
            else:
                raise HTTPError("Request was not successful.")
    return urls


def fetch_games(url):
    """Fetch table of a website.

    Arg: url of the website as string

    Functionality: Function parses through website to find a table, then stores This
    table as a DataFrame.

    Out: DataFrame
    """
    # make soup
    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    # use findALL() to get the column headers
    soup.findAll("tr", limit=2)

    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]

    # avoid the first header row
    rows = soup.findAll("tr")[1:]
    games = [[td.getText() for td in rows[i]] for i in range(len(rows))]

    # Convert into Dataframe
    month = pd.DataFrame(games, columns=headers)
    return month
