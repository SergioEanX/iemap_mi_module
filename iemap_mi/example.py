import asyncio
# import getpass
import stdiomask
from iemap_mi import IemapMI


async def main():
    # Initialize the client
    client = IemapMI()

    # Fetch statistics data
    stats = await client.stat_handler.get_stats()
    print(stats.model_dump())

    # Prompt for username and password
    username = input("Enter your username (email address): ")
    password = stdiomask.getpass(prompt="Enter your password: ")

    # Authenticate to get the JWT token
    await client.authenticate(username=username, password=password)

    # Fetch paginated project data
    projects = await client.project_handler.get_projects(page_size=10, page_number=1)
    print(projects)

    client.stat_handler.get_stats()


if __name__ == "__main__":
    asyncio.run(main())
