import httpx
from typing import Optional, Dict, Any
from iemap_mi.models import ProjectResponse, CreateProjectRequest, CreateProjectResponse
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


async def create_project(self, project_data: CreateProjectRequest) -> CreateProjectResponse:
    """
    Create a new project.

    Args:
        project_data (CreateProjectRequest): Data for the new project.

    Returns:
        CreateProjectResponse: Response containing the inserted ID of the new project.
    """
    endpoint = f"{self.base_url}/api/v1/project/add"
    headers = get_headers(self.token)

    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=project_data.dict(), headers=headers)
        response.raise_for_status()
        return CreateProjectResponse(**response.json())


async def add_file_to_project(self, project_id: str, file_path: str, file_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a file to a project.

    Args:
        project_id (str): The ID of the project to add the file to.
        file_path (str): The path to the file to be uploaded.
        file_name (Optional[str]): The name of the file. Defaults to None.

    Returns:
        Dict[str, Any]: Response from the API.
    """
    endpoint = f"{self.base_url}/api/v1/project/add/file/"
    headers = get_headers(self.token)
    params = {"project_id": project_id}
    if file_name:
        params["file_name"] = file_name

    allowed_extensions = {"pdf", "doc", "docs", "xls", "xlsx", "rt", "cif", "dat", "csv", "png", "jpg", "tif"}
    if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
        raise ValueError(f"File extension not allowed. Allowed extensions are: {', '.join(allowed_extensions)}")

    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as file:
            files = {"file": (file_name or file_path, file)}
            response = await client.post(endpoint, params=params, headers=headers, files=files)
            response.raise_for_status()
            return response.json()
