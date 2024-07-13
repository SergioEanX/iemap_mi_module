from typing import Optional, Dict, Any
import httpx
from iemap_mi.models import StatsResponse
from iemap_mi.utils import get_headers


class IemapStat:
    def __init__(self, base_url: str, token: Optional[str] = None) -> None:
        """
        Initialize IemapStat with base URL and JWT token.

        Args:
            base_url (str): Base URL for the API.
            token (Optional[str]): JWT token for authentication. Defaults to None.
        """
        self.base_url = base_url
        self.token = token

    async def get_stats(self) -> StatsResponse:
        """
        Get statistics from the API.

        Returns:
            StatsResponse: Response containing statistics data.
        """
        endpoint = f"{self.base_url}/api/v1/stats"
        headers = get_headers(self.token)

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            return StatsResponse(**response.json())
