import pytest
from iemap_mi.iemap_mi import IemapMI


@pytest.mark.asyncio
async def test_authenticate(credentials: tuple[str, str]) -> None:
    """
    Test user authentication.

    Args:
        credentials (tuple[str, str]): Tuple containing username and password.
    """
    username, password = credentials
    client = IemapMI()
    await client.authenticate(username=username, password=password)
    assert client.token is not None


@pytest.mark.asyncio
async def test_get_example_data(credentials: tuple[str, str]) -> None:
    """
    Test fetching example data.

    Args:
        credentials (tuple[str, str]): Tuple containing username and password.
    """
    username, password = credentials
    client = IemapMI()
    await client.authenticate(username=username, password=password)
    data = await client.get_example_data()
    assert data is not None


@pytest.mark.asyncio
async def test_get_projects(credentials: tuple[str, str]) -> None:
    """
    Test fetching paginated list of projects.

    Args:
        credentials (tuple[str, str]): Tuple containing username and password.
    """
    username, password = credentials
    client = IemapMI()
    await client.authenticate(username=username, password=password)
    projects = await client.project_handler.get_projects(page_size=10, page_number=1)
    assert projects is not None
    assert 'data' in projects.dict()
