from typing import Optional
import httpx
from iemap_mi.models import ProjectResponse
from iemap_mi.utils import get_headers


class ProjectHandler:
    def __init__(self, base_url: str, token: Optional[str] = None) -> None:
        """
        Initialize ProjectHandler with base URL and JWT token.

        Args:
            base_url (str): Base URL for the API.
            token (Optional[str]): JWT token for authentication. Defaults to None.
        """
        self.base_url = base_url
        self.token = token

    async def get_projects(self, page_size: int = 10, page_number: int = 1) -> ProjectResponse:
        """
        Get paginated list of projects.

        Args:
            page_size (int): Number of results to return in a single page. Defaults to 10.
            page_number (int): Actual page number returned. Defaults to 1.

        Returns:
            ProjectResponse: Paginated list of projects.
        """
        endpoint = f"{self.base_url}/api/v1/project/list/"
        params = {'page_size': page_size, 'page_number': page_number}
        headers = get_headers(self.token)

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return ProjectResponse(**response.json())
