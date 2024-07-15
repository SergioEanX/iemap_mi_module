import asyncio
# import getpass
import stdiomask
from pydantic import TypeAdapter
from iemap_mi import IemapMI
from typing import List, Union
from iemap_mi.models import (CreateProjectRequest, Project, Material, Process, Agent,
                             Parameter, Property, FlattenedProjectBase, FlattenedProjectHashEmail)
from iemap_mi.project_handler import ProjectHandler
from iemap_mi.utils import flatten_project_data

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from tqdm import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


async def iterate_projects(client: IemapMI, page_size: int = 40, show_email: bool = False) -> None:
    """Iterate over projects and print them or convert to pandas DataFrame if available."""
    page_number = 1
    all_projects: List[FlattenedProjectBase] = []
    total_projects = None  # Initialize total_projects to None

    while True:
        projects_response = await client.project_handler.get_projects(page_size=page_size, page_number=page_number)
        if not projects_response.data:
            break

        if show_email:
            adapter = TypeAdapter(FlattenedProjectBase)
        else:
            adapter = TypeAdapter(FlattenedProjectHashEmail)

        projects = [adapter.validate_python(project) for project in projects_response.data]

        all_projects.extend(projects)
        page_number += 1

        if total_projects is None:
            total_projects = projects_response.number_docs

        if TQDM_AVAILABLE:
            tqdm.write(f"Page {page_number - 1} fetched. Total projects so far: {len(all_projects)}/{total_projects}")

    if PANDAS_AVAILABLE:
        # Set the option to display all columns
        pd.set_option('display.max_columns', None)
        # Convert the projects to a pandas DataFrame
        # df = pd.DataFrame([project.model_dump() for project in all_projects])
        flat_projects = [flatten_project_data(project) for project in all_projects]
        df = pd.DataFrame(flat_projects)
        print(df)
    else:
        # Print the projects as a list of dictionaries
        for project in all_projects:
            print(project.model_dump())


async def main():
    # Initialize the client
    client = IemapMI()

    # Print the module version
    IemapMI.print_version()

    # Iterate over projects and print them or convert to pandas DataFrame if available
    # await iterate_projects(client, page_size=60, show_email=False)

    # Fetch statistics data
    stats = await client.stat_handler.get_stats()
    print(stats.model_dump())

    query_response = await client.project_handler.query_projects(
        # project_name="Materials for Batteries",
        isExperiment=True,
        limit=10
    )

    print([doc.model_dump() for doc in query_response])

    # Prompt for username and password
    username = input("Enter your username (email address): ")
    password = stdiomask.getpass(prompt="Enter your password: ")

    # Authenticate to get the JWT token
    # ATTENTION: you should register to the IEMAP platform to get your credentials (that has to be validated)
    # To do so, please visit: https://iemap.enea.it/auth/signup

    await client.authenticate(username=username, password=password)

    # Define the project metadata, for example:
    data = {
        "project": {
            "name": "Materials for Batteries",
            "label": "MB",
            "description": "IEMAP - eco-sustainable synthesis of ionic liquids as innovative solvents for lithium/sodium batteries"
        },
        "material": {
            "formula": "C11H20N2F6S2O4"
        },
        "process": {
            "method": "Karl-Fischer titration",
            "agent": {
                "name": "Karl-Fischer titrator Mettler Toledo",
                "version": None
            },
            "isExperiment": True
        },
        "parameters": [
            {
                "name": "time",
                "value": 20,
                "unit": "s"
            },
            {
                "name": "weight",
                "value": 0.5,
                "unit": "gr"
            }
        ],
        "properties": [
            {
                "name": "Moisture content",
                "value": "<2",
                "unit": "ppm"
            }
        ]
    }

    # Build and validate the project payload
    valid_payload_example_1 = ProjectHandler.build_project_payload(data)

    if valid_payload_example_1:
        print("Payload is valid and ready to be submitted.")
    else:
        print("Payload is invalid.")

    # Example of invalid payload
    data_invalid = {"project": {
        "name": "Materials for Batteries",
        "label": "MB",
        # "description": Description is missing this is  a required field !!!
    },
        # material is missing and this is a required field !!!!
        # "material": {
        #     "formula": "C11H20N2F6S2O4"
        # },
        "process": {
            "method": "Karl-Fischer titration",
            "agent": {
                "name": "Karl-Fischer titrator Mettler Toledo",
                "version": None
            },
            "isExperiment": True
        }}
    # Also missing are parameters and properties, which are required fields

    # Build and validate the project payload
    # as the payload is invalid, the function will return None and print the error message that caused the payload to be invalid
    # in this case, the error message is:
    #
    # Validation Error: The provided data is not valid.
    # Error in field 'project.description': Field required (type: missing)
    # Error in field 'material': Field required (type: missing)
    # Error in field 'parameters': Field required (type: missing)
    # Error in field 'properties': Field required (type: missing)

    valid_payload_example_2 = ProjectHandler.build_project_payload(data_invalid)

    if valid_payload_example_2:
        print("Payload from 'data_invalid' is valid and ready to be submitted.")
    else:
        print("Payload from 'data_invalid' is invalid.")

    if valid_payload_example_1:
        # Create a new project
        new_project = await client.project_handler.create_project(valid_payload_example_1)
        print(new_project)

        # Add a file to the project
        file_response = await client.project_handler.add_file_to_project(
            project_id=new_project.inserted_id,
            file_path="/path/to/your/file.pdf",
            file_name="file.pdf"
        )
        print(file_response)

    # Create a new project
    project_data = CreateProjectRequest(
        project=Project(
            name="Materials for Batteries",
            label="MB",
            description="IEMAP - eco-sustainable synthesis of ionic liquids as innovative solvents for lithium/sodium batteries"
        ),
        material=Material(
            formula="C11H20N2F6S2O4"
        ),
        process=Process(
            method="Karl-Fischer titration",
            agent=Agent(
                name="Karl-Fischer titrator Mettler Toledo",
                version=None
            ),
            isExperiment=True
        ),
        parameters=[
            Parameter(
                name="time",
                value=20,
                unit="s"
            ),
            Parameter(
                name="weight",
                value=0.5,
                unit="gr"
            )
        ],
        properties=[
            Property(
                name="Moisture content",
                value="<2",
                unit="ppm"
            )
        ]
    )

    new_project = await client.project_handler.create_project(project_data)
    print(new_project)

    # Add a file to the project
    file_response = await client.project_handler.add_file_to_project(
        project_id=new_project.inserted_id,
        file_path="/path/to/your/file.pdf",
        file_name="file.pdf"
    )
    print(file_response)

    # Fetch statistics data
    client.stat_handler.get_stats()


if __name__ == "__main__":
    asyncio.run(main())
