# Predicting Basketball Games

After webscraping basketball-reference.com, the data is used to provide the season
averages of PTS and Wins/Losses for each team up to the date they play. Next,
machine learning algorithms are used, first, to determine which factors can predict
basketball games best and in the next step use the best dataset and the best algorithm
to predict games withheld from testing.

## Getting Started

The further instructions will guide you along to how the project can be set up and run.

### Dependencies

The project runs in an conda environment. The various dependencies can be checked in the
environment.yml file.
To get the environment up and running:

```
Conda env create -f environment.yml

conda activate predict_bball
```
It was run on the following machine:

```
Macbook Pro
Version:
Processor:
```

### Running tests

To ensure consistency within the project, tests are constructed on numerous stages.They can be called with:

```
pytest
```

## Deployment

The project runs with waf, yet before applying the waf machinery the webscraping
has to be done. The files that will be downloaded during the process are already in the intended folder but feel free
to test out the scraper. Then, waf can be run to spit out the analysis. The scraper can be run as follows:

```
python src/webscraper/schedule_scraper.py
```

### Robots.txt

The scraper adheres to the TOS of basketball-reference.com and makes "no more requests than a typical human could", also a crawl-delay of three seconds as specified in the robots.txt is followed.

## Acknowledgments

* Many unsung heroes in the web, whose code was used

* To xyz for their inspiration using similar techniques to predict basketball games
