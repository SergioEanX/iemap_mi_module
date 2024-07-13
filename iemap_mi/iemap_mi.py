# iemap_mi/iemap_mi.py

from typing import Optional, Dict, Any
import httpx
from pydantic import HttpUrl
from iemap_mi.project_handler import ProjectHandler
from iemap_mi.iemap_stat import IemapStat
from iemap_mi.models import AuthData
from iemap_mi.utils import get_headers


class IemapMI:
    def __init__(self, base_url: HttpUrl = 'https://iemap.enea.it/rest') -> None:
        """
        Initialize IemapMI with base URL.

        Args:
            base_url (HttpUrl): Base URL for the API.
        """
        self.base_url = base_url
        self.token: Optional[str] = None
        self.project_handler = ProjectHandler(base_url, self.token)
        self.stat_handler = IemapStat(base_url, self.token)

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a GET request to the specified endpoint.

        Args:
            endpoint (str): API endpoint to make the GET request to.
            params (Optional[Dict[str, Any]]): Query parameters for the request. Defaults to None.

        Returns:
            Any: Response from the GET request.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = get_headers(self.token)

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    async def authenticate(self, username: str, password: str) -> None:
        """
        Authenticate the user and obtain a JWT token.

        Args:
            username (str): Username for authentication.
            password (str): Password for authentication.
        """
        auth_data = AuthData(username=username, password=password)
        endpoint = 'auth/jwt/login'
        url = f"{self.base_url}/{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=auth_data.dict())
            response.raise_for_status()
            self.token = response.json().get('access_token')
            # Update the token in the project and stat handlers
            self.project_handler.token = self.token
            self.stat_handler.token = self.token

    async def get_example_data(self) -> Any:
        """
        Get example data from a specific endpoint.

        Returns:
            Any: Example data from the specified endpoint.
        """
        endpoint = 'example_endpoint'
        params = {'key': 'value'}
        return await self._get(endpoint, params)
