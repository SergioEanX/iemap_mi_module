![Project Logo](https://github.com/SergioEanX/iemap_mi_module/blob/master/images/logo_iemap.png?raw=True)
# Iemap-MI Python Module

[![PyPI version](https://badge.fury.io/py/iemap-mi.svg)](https://badge.fury.io/py/iemap-mi)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Iemap-MI is a Python module that provides easy access to the IEMAP REST API. It includes functionality for user
authentication, fetching paginated project data, and more. The module is designed to be used asynchronously and
leverages `httpx` for making HTTP requests and `pydantic` for data validation.

## Features

- **JWT Authentication**: Authenticate users and manage sessions with JSON Web Tokens.
- **Project Data**: Fetch paginated project data from the API.
- **Asynchronous Requests**: Utilize `httpx` for efficient, asynchronous HTTP requests.
- **Data Validation**: Ensure data integrity with `pydantic` models.

## Installation

To install the module, use `poetry`:

```sh
poetry add iemap-mi
```

Alternatively, you can install it using pip:

```sh

pip install iemap-mi
```

## Usage

Here are some examples of how to use the iemap-mi module.

### Initialize the Client and Authenticate

```python

import asyncio
from iemap_mi.iemap_mi import IemapMI


async def main():


# Initialize the client
client = IemapMI()

# Authenticate to get the JWT token
await client.authenticate(username='your_username', password='your_password')

# Fetch example data
data = await client.get_example_data()
print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

### Fetch Paginated Project Data

```python

import asyncio
from iemap_mi.iemap_mi import IemapMI


async def main():


# Initialize the client
client = IemapMI()

# Authenticate to get the JWT token
await client.authenticate(username='your_username', password='your_password')

# Fetch paginated project data
projects = await client.project_handler.get_projects(page_size=10, page_number=1)
print(projects)

if __name__ == "__main__":
    asyncio.run(main())
```

### Running Tests

To run the tests, use pytest. Make sure to set the TEST_USERNAME and TEST_PASSWORD environment variables with your test
credentials.

```sh

export TEST_USERNAME="your_username"
export TEST_PASSWORD="your_password"
pytest
```

Using pytest with poetry

```sh

poetry run pytest
```

Contributing

Contributions are welcome! Please follow these steps to contribute:

    Fork the repository.
    Create a new branch for your feature or bugfix.
    Make your changes.
    Ensure tests pass.
    Submit a pull request.

License

This project is licensed under the MIT License.   
See the LICENSE file for more information.   
Acknowledgements

    httpx
    pydantic

Contact

For any questions or inquiries, please contact iemap.support@enea.it.

```typescript
This`README.md`
includes
an
overview
of
the
project, installation
instructions,
    usage
examples, testing
guidelines, contribution
guidelines, license
information,
    acknowledgements, and
contact
information.
```