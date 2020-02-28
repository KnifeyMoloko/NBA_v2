"""
Conftest fixtures adding runtime CLI args for NBA_v2 app
Author: Maciej Cisowski
"""
import pytest


def pytest_addoption(parser):
    """
    Add start and end dates for the program run to use.
    :param parser:
    :return:
    """
    parser.addoption(
        "--NBASTARTDATE", action="store", default="2019/10/22", help="start date"
    )
    parser.addoption(
        "--NBAENDDATE", action="store", default="2019/10/22", help="end date"
    )


@pytest.fixture(scope='session')
def sdate(request):
    # Adds start date as a usable variable for tests
    return request.config.getoption("NBASTARTDATE")


@pytest.fixture(scope='session')
def edate(request):
    # Adds end date as a usable variable for tests
    return request.config.getoption("NBAENDDATE")
