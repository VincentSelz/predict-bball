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
To get the environment up and running, one has navigate to the parent folder via the command line and type:

```
$ conda env create -f environment.yml

$ conda activate predict_bball
```
It was run on a MacOS Sierra Version 10.13


### Running tests

To ensure consistency within the project, some tests are constructed. They can be called with:

```
$ pytest
```
Note that these tests focus on the scraper. Time permitting, I'll expand the test coverage towards the other parts of my project.

## Deployment

The project runs with waf, yet before applying the waf machinery the webscraping
has to be done. The files that will be downloaded during the process are already in the intended folder but feel free
to test out the scraper. Then, waf can be run to spit out the analysis. The scraper can be run as follows:

```
$ python src/webscraper/schedule_scraper.py
```

### Robots.txt

The scraper adheres to the TOS of basketball-reference.com and makes "no more requests than a typical human could", also a crawl-delay of three seconds as specified in the robots.txt is followed.

### Waf

In order to run waf, one has to type:

```
$ python waf.py configure

$ python waf.py build
```
Depending on the machine, this can take up to five minutes. Afterwards, the analysis can be found in the bld-folder.
