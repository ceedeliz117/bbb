import pytest
from django.conf import settings

@pytest.mark.django_db
def test_django_setup():
    assert settings.configured
    assert 'core' in settings.INSTALLED_APPS
