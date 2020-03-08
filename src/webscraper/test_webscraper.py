import pytest
from helper_functions import get_URLs
from schedule_scraper import schedule_scraper


def test_get_URLs_typical_input():
    urls = get_URLs(2014)
    assert len(urls) == 9


def test_schedule_scraper_valid_years():
    """tests whether specified years are a subset of the available years of data."""
    with pytest.raises(ValueError):
        schedule_scraper([1891, 1999])


def test_get_URLs_is_integer():
    with pytest.raises(ValueError):
        get_URLs(2014.5)
