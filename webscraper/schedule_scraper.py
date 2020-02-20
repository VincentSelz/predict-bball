"""This program scrapes basketball-reference.com to attain the scores
for each game in the specified season and exports them as excel files.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql
import pandas as pd
import requests
import time
