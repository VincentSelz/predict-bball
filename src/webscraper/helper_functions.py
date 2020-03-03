"""Helper functions.
"""
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

# from bld.project_paths import project_paths_join as ppj


def get_URLs(year):
    """get the working URLs for the website and store them in a list.

    Args: year

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
        try:
            url = (
                f"https://www.basketball-reference.com/"
                "leagues/NBA_{}_games-{}.html".format(year, month)
            )

            urls.append(url)
        except HTTPError as err:
            if err.code == 404:
                continue
            else:
                raise HTTPError("Request was not successful.")
    return urls


def fetch_games(url):
    """Fetch first table of the website with specified table headers and turn it
    into a Dataframe.

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
