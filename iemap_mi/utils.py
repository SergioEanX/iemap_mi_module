from typing import Optional, Dict


def get_headers(token: Optional[str]) -> Dict[str, str]:
    """
    Generate headers for HTTP requests.

    Args:
        token (Optional[str]): JWT token for authentication.

    Returns:
        Dict[str, str]: Headers for HTTP requests.
    """
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    return headers
