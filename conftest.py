import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--NBASTARTDATE", action="store", default="2019/10/22", help="start date"
    )
    parser.addoption(
        "--NBAENDDATE", action="store", default="2019/10/22", help="end date"
    )


@pytest.fixture(scope='session')
def sdate(request):
    return request.config.getoption("NBASTARTDATE")


@pytest.fixture(scope='session')
def edate(request):
    return request.config.getoption("NBAENDDATE")
