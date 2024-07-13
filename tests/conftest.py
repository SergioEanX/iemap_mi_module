# tests/conftest.py
import os
import pytest


@pytest.fixture
def credentials() -> tuple[str, str]:
    username = os.getenv("TEST_USERNAME", "default_username")
    password = os.getenv("TEST_PASSWORD", "default_password")
    return username, password
