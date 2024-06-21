import pytest

@pytest.fixture(autouse=True, scope='session')
def django_db_setup():
    pass
