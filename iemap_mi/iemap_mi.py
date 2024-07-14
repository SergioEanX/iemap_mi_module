# iemap_mi/iemap_mi.py
import asyncio
import logging
import httpx
from typing import Optional, Dict, Any
from pydantic import HttpUrl
from iemap_mi.project_handler import ProjectHandler
from iemap_mi.iemap_stat import IemapStat
from iemap_mi.__version__ import __version__
from iemap_mi.settings import settings


class IemapMI:
    def __init__(self) -> None:
        """
        Initialize IemapMI with base URL.

        Args:
            base_url (HttpUrl): Base URL for the API.
        """

        self.token: Optional[str] = None
        self.project_handler = ProjectHandler(self.token)
        self.stat_handler = IemapStat(self.token)

    async def authenticate(self, username: str, password: str) -> None:
        """
           Authenticate the user and obtain a JWT token.

           Args:
               username (str): Username for authentication.
               password (str): Password for authentication.
           """
        endpoint = settings.AUTH_JWT_LOGIN
        data = {
            'username': username,
            'password': password
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, data=data)
            response.raise_for_status()
            self.token = response.json().get('access_token')
            # Update the token in the project and stat handlers
            self.project_handler.token = self.token
            self.stat_handler.token = self.token

    @staticmethod
    def handle_exception(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
        """
        Handle exceptions in asyncio.

        Args:
            loop (asyncio.AbstractEventLoop): The event loop.
            context (Dict[str, Any]): The exception context.
        """
        logging.error(f"Caught exception: {context['message']}")
        exception = context.get("exception")
        if exception:
            logging.error(f"Exception: {exception}")

    @staticmethod
    def print_version() -> None:
        """
        Print the version of the IemapMI module.
        """
        print(f"IemapMI version: {__version__}")
