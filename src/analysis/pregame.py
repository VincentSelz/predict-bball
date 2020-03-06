"""This script reads in data cleans/curates it and does first steps toward analyzing it."""


def dropNaNs(df):
    """Drops missing values when they are at the start of the season.

    Args: dataset

    Notes: for the first game of a season a team has no historic data,
    hence missing values. Function missing only but only at the start of a season.
    """
    nans = df[df.isnull().any(axis=1)]
    if nans.gameid.all() < 30:
        clean_data = df.dropna()
    else:
        raise ValueError("Values are missing, where they should not")
    return clean_data


def order_dataset(df):
    """Get dataframe, order it.

    Args: dataset
    """
    df = df.reindex(
        columns=[
            "gameid",
            "Date",
            "Away Team",
            "PTS Away",
            "Home Team",
            "PTS Home",
            "Win Difference",
            "Home Win",
            "Games No Home Team",
            "Games No Away Team",
            "Home Wins",
            "Away Wins",
            "Home Losses",
            "Away Losses",
            "Home PTS Average",
            "Away PTS Average",
            "Home OPP PTS Average",
            "Away OPP PTS Average",
            "Home Win Percentage",
            "Away Win Percentage",
            "Home Point Differential",
            "Away Point Differential",
            "Home Days Off",
            "Away Days Off",
        ]
    )
    return df


def get_datasets(df):
    datasets = []
    totals = df.drop(df.columns[[1, 2, 7, 8, 9, 10, 11, 12, 13, 14]], axis=1)
    datasets.append(("Totals", totals))
    perc_diff = df.drop(df.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], axis=1)
    datasets.append(("Win Percentage + Point Differential", perc_diff))
    perc_average = df.drop(df.columns[[1, 2, 3, 4, 5, 6, 13, 14]], axis=1)
    datasets.append(("Win Percentage + Per Game Averages", perc_average))
    perc_average_woDaysOff = df.drop(
        df.columns[[1, 2, 3, 4, 5, 6, 13, 14, 15, 16]], axis=1
    )
    datasets.append(
        ("Win Percentage + Per Game Averages without Days Off", perc_average_woDaysOff)
    )
    perc_diff_woDaysOff = df.drop(
        df.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16]], axis=1
    )
    datasets.append(
        ("Win Percentage + Point Differential without Days Off", perc_diff_woDaysOff)
    )
    return datasets
