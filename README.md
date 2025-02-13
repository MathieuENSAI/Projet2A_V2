# Réseau social Ciné 🍿

## Project Overview

"Réseau social Cinéma" is a web service that allows users to interact with their movie preferences and explore films through social connections.

### Users can:

- Create an account.  
- Add movies to their favorites and watchlists
- Rate movies and track their viewing history.
- Follow other users and view their movie collections.
- Discover films that have been watched by both the user and those they follow.

### Authenticated users have access to :

- Personalized and detailed data, including the ability to rate movies and manage their collections.
- Suggestions for new follows.
- The platform ensures that only valid, authenticated users can perform actions like rating or following.
- Additionally, the project integrates social features, allowing users to engage with others' movie choices, share collections, and collaborate on discovering new films together.

## Prerequisite: PDM

PDM (Python Development Master) is a modern Python package manager that simplifies dependency management and virtual environment handling. The project uses PDM for managing dependencies and virtual environments.

### Install PDM
To install PDM for your user with pip, run the following command:

> pip install --user pdm

You can check if PDM is installed correctly by running:

> pdm --version

### In case of pdm: command not found

If you encounter the error pdm: command not found, you need to add the PDM executable to your system's PATH environment variable.

### To do so:

- Locate the folder where PDM was installed by running pip list -v (typically in a path like C:/Users/YourUsername/AppData/Roaming/Python/Python310/site-packages).

- Find the Scripts folder, which is located alongside site-packages (e.g., C:/Users/YourUsername/AppData/Roaming/Python/Python310/Scripts), and copy this path.

- On Windows, search for "Edit the system environment variables".

- In the System Properties window, click on Environment Variables, then find the Path variable in the User variables section.

- Edit the Path variable and add the copied folder path at the end, then save.
Afterward, open a new terminal and retry the pdm command.

## How to install the app

Once you have installed PDM, you can install all the required dependencies for the project using the following command:

> pdm install

This will install the dependencies listed in the pyproject.toml file, which includes libraries such as FastAPI, Uvicorn, Pydantic, and others necessary for the application to run.

For a list of all dependencies, check the pyproject.toml file.

## How to run the app

To start the application, run:

> pdm start

This will launch the server, and the application will be accessible at localhost:8000. The API documentation can be viewed at localhost:8000/docs.

## Project Dependencies

The project uses several key dependencies, all of which are defined in the pyproject.toml file. These include:

- FastAPI: A modern, fast web framework for building APIs.

- Uvicorn: An ASGI server for running FastAPI applications.

- Pydantic: Used for data validation and parsing.

- PyJWT: Used for handling JSON Web Tokens for authentication.

- psycopg2-binary: PostgreSQL database adapter.

- python-dotenv: For managing environment variables securely.

## Dev Dependencies

In addition to the main dependencies, the project includes the following development dependencies for testing, linting, and type checking:

- pytest: A testing framework.

- pytest-cov: For test coverage.

- freezegun: For freezing time during tests.

You can see the full list of dependencies and their versions in the pyproject.toml file.

## Testing

To run the tests for this project, execute the following command:

> pdm run test

This will run all the tests in the tests folder using pytest.