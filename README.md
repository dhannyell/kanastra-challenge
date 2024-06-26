# Backend Challenge [![CircleCI](https://dl.circleci.com/status-badge/img/circleci/SdtpWkQEvBq7VADRHZsRm/HoQr7zpC4VGreQDKm3EnxX/tree/main.svg?style=svg)](https://app.circleci.com/pipelines/circleci/SdtpWkQEvBq7VADRHZsRm/HoQr7zpC4VGreQDKm3EnxX?branch=main) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dhannyell/kanastra-challenge/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/dhannyell/kanastra-challenge/?branch=main)

Hiring Challenge (Soft. Engineers Backend) - Take Home

## Table of Contents

1. [Dependencies](#dependencies)
1. [Getting Started](#getting-started)
1. [Commands](#commands)
1. [Database](#database)
1. [Application Structure](#application-structure)
1. [Development](#development)
1. [Testing](#testing)
1. [Lint](#lint)
1. [Format](#format)
1. [Swagger](#swagger)

## Dependencies

You will need [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

## Getting Started

First, clone the project:

```bash
$ git clone https://github.com/dhannyell/kanastra-challenge.git <my-project-name>
$ cd <my-project-name>
```

Then install dependencies and check that it works

```bash
$ make server.install      # Install the pip dependencies on the docker container
$ make server.start        # Run the container containing your local python server
```

currently the project only has the route: api/upload-file.

add the conten-type for multipart/form-data in the request header and send the csv file as multipart file

If everything works, you should see the available routes [here](http://127.0.0.1:3000/application/spec).

The API runs locally on docker containers. You can easily change the python version you are willing to use [here](https://github.com/dhannyell/kanastra-challenge/blob/main/docker-compose.yml#L4), by fetching a docker image of the python version you want.

## CICD

This project has a complete implementation of CICD using CircleCI to build the application and Scrutinizer to check the quality of the Code.

At the beginning of the Readme it is possible to check the status of the latest build of the project.

## Commands

You can display availables make commands using `make`.

While developing, you will probably rely mostly on `make server.start`; however, there are additional scripts at your disposal:

| `make <script>`      | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| `help`               | Display availables make commands                                             |
| `server.install`     | Install the pip dependencies on the server's container.                      |
| `server.start`       | Run your local server in its own docker container.                           |
| `server.daemon`      | Run your local server in its own docker container as a daemon.               |
| `server.upgrade`     | Upgrade pip packages interactively.                                          |
| `database.connect`   | Connect to your docker database.                                             |
| `database.migrate`   | Generate a database migration file using alembic, based on your model files. |
| `database.upgrade`   | Run the migrations until your database is up to date.                        |
| `database.downgrade` | Downgrade your database by one migration.                                    |
| `test`               | Run unit tests with pytest in its own container.                             |
| `test.coverage`      | Run test coverage using pytest-cov.                                          |
| `test.lint`          | Run flake8 on the `src` and `test` directories.                              |
| `test.safety`        | Run safety to check if your vendors have security issues.                    |
| `format.black`       | Format python files using Black.                                             |
| `format.isort`       | Order python imports using isort.                                            |

## Database

The database is in [PostgreSql](https://www.postgresql.org/).

Locally, you can connect to your database using :

```bash
$ make database.connect
```

However, you will need before using this command to change the docker database container's name [here](https://github.com/dhannyell/kanastra-challenge/blob/main/package.json#L6).

This kit contains a built in database versioning using [alembic](https://pypi.python.org/pypi/alembic).
Once you've changed your models, which should reflect your database's state, you can generate the migration, then upgrade or downgrade your database as you want. See [Commands](#commands) for more information.

The migration will be generated by the container, it may possible that you can only edit it via `sudo` or by running `chown` on the generated file.

## Application Structure

The application structure presented in this boilerplate is grouped primarily by file type. Please note, however, that this structure is only meant to serve as a guide, it is by no means prescriptive.

```
.
├── devops                          # Project devops configuration settings
│   └── deploy                      # Environment-specific configuration files for shipit
├── migrations                      # Database's migrations settings
│   └── versions                    # Database's migrations versions generated by alembic
├── src                             # Application source code
│   ├── application_layer       
│   │   ├── adapter                 # Services Layer and repository
│   │   │   ├── boleto_service.py
│   │   │   ├── debit_repository
│   │   │   ├── email_service 
│   │   ├── persistency             # Defining how data will be represented in the database
│   │   │    └── debit.py
│   │   ├── use_cases               # Backend logic
│   │       └── debit.py
│   ├── domain_layer                # Transition Layer between views and services
│   │   ├──abstract                 # Definition of the abstracted classes
│   │   │  ├──boleto.py
│   │   │  ├──debit.py
│   │   │  ├──email.py  
│   │   ├──models                   # Definition of Models used in the application
│   │   │  ├──boleto.py
│   │   │  ├──debit.py
│   │   │  ├──email.py              
│   ├── presentation_layer          # Layer responsible for receiving requests and responding to the user
│   │   └──views                    
│   │   │  └──index.py              # Route logic
│   │   ├──mapping.py               # Maps how request data will be handled
        ├──schemas.py               # Describes the models accepted in the request
│   ├── swagger                     # Resources documentation
│   │       └── PUT.yml             # Documentation of the PUT method
│   ├── util                        # Some helpfull, non-business Python functions
│   │   └── verify_header.py        # Wrapper to check if the header is correct
│   ├── config.py                   # Project configuration settings
│   ├── manage.py                   # Project commands
│   └── server.py                   # Server configuration
└── test                            # Unit tests source code
```

## Development

To develop locally, here are your two options:

```bash
$ make server.start           # Create the containers containing your python server in your terminal
$ make server.daemon          # Create the containers containing your python server as a daemon
```

The containers will reload by themselves as your source code is changed.
You can check the logs in the `./server.log` file.

## Testing

To add a unit test, simply create a `test_*.py` file anywhere in `./test/`, prefix your test classes with `Test` and your testing methods with `test_`. Unittest will run them automaticaly.
You can add objects in your database that will only be used in your tests, see example.
You can run your tests in their own container with the command:

```bash
$ make test
```

## Lint

To lint your code using flake8, just run in your terminal:

```bash
$ make test.lint
```

It will run the flake8 commands on your project in your server container, and display any lint error you may have in your code.

## Format

The code is formatted using [Black](https://github.com/python/black) and [Isort](https://pypi.org/project/isort/). You have the following commands to your disposal:

```bash
$ make format.black # Apply Black on every file
$ make format.isort # Apply Isort on every file
```

## Swagger

Your API needs a description of it's routes and how to interact with them.
You can easily do that with the swagger package included in the starter kit.
Simply add a docstring to the resources of your API.
The API description will be available [here](http://127.0.0.1:3000/application/spec).
The Swagger UI will be available [here](http://127.0.0.1:3000/apidocs/).
