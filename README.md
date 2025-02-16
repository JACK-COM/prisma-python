# Mythia API

Python backend for the Mythia project. Based on [JACKOM's Prisma-Python project template](https://github.com/JACK-COM/prisma-python).\
See [dependencies](#dependencies) for the list, as well as documentation links.

If you are familiar with any of the [dependencies](#dependencies) and/or Python, it should be straightforward to use. It should also be somewhat familiar if you have used `Prisma` with JS.

## Table of Contents

- [Mythia API](#mythia-api)
  - [Table of Contents](#table-of-contents)
  - [Development](#development)
    - [1. Initial Environment Setup](#1-initial-environment-setup)
    - [2. Install project dependencies with uv](#2-install-project-dependencies-with-uv)
    - [3. Run the project](#3-run-the-project)
      - [Development Environment](#development-environment)
    - [4. Table Changes and Database Migrations](#4-table-changes-and-database-migrations)
      - [Run prisma migrations WITHOUT starting the server](#run-prisma-migrations-without-starting-the-server)
      - [Start API Server without prisma migrations](#start-api-server-without-prisma-migrations)
  - [Dependencies](#dependencies)
    - [What is uv?](#what-is-uv)
    - [Adding dependencies with uv](#adding-dependencies-with-uv)
    - [Additional uv scripts](#additional-uv-scripts)
  - [Troubleshooting](#troubleshooting)
    - [Resolve dependency paths in VSCode](#resolve-dependency-paths-in-vscode)
    - [Silent migration failure when adding Enums](#silent-migration-failure-when-adding-enums)

## Development

### 1. Initial Environment Setup

After initially cloning the repository, follow the steps outlined [**here**](./PRE_SETUP.md) to set up you environment and database, as well as configure your `.env` file.

### 2. Install project dependencies with uv

Since this is Python, you will need to set up and activate a new virtual environment before adding dependencies.

Run the following in the project root (where `pyproject.toml` can be found) to install project dependencies from the included `uv.lock` file. See [additional scripts](#additional-uv-scripts) for commands to update one or more dependencies.

If you have `make` installed, you can use the following convenience command:

```bash
make add-deps
```

If you don't have `make` installed, run these three commands:

```bash
# 3. Install dependencies
$. uv pip install -r pyproject.toml 
```

### 3. Run the project

#### Development Environment

Run the following in the project root (where `pyproject.toml` can be found).\
This will run the application in dev mode on port `8000`.

If you have `make` installed, you can use the following convenience command:

```bash
$. make start
```

If you don't have `make`, use the following command:

```bash
$. uv run dev.py
```

### 4. Table Changes and Database Migrations

To add (or change) your database:

1. Modify the `schema.prisma` file (add tables/columns/etc) and save your changes
2. Restart the app and include the `--migrate` flag to apply changes to the database before the server starts up.

This allows you to sync your changes by simply re-starting the dev server. Migration history will be squashed into a single file, so that the `migrations/` directory stays small and manageable.

`dev.py` accepts an optional `--migrate` boolean flag that triggers a prisma migration to sync your db with the `schema.prisma` file before starting up. (see below)

If you have `make` installed, you can use the following convenience command:

```bash
$. make migrate-start
```

If you don't have `make` installed, run this command instead:

```bash
$. uv run dev.py --migrate
```

#### Run prisma migrations WITHOUT starting the server

You can run migrations alone without starting or re-starting the server.

```bash
$. uv run scripts/db_migrate.py
```

If you have `make` installed, you can use the following convenience command:

```bash
$. make migrate
```

#### Start API Server without prisma migrations

If you don't want to use the prisma migration script, any of the following commands will start the server. With make installed:

```bash
# call fastapi with uv
$. make start
```

Without `make` installed, you can use any ONE of the following:

```bash
# 1. Preferred: call fastapi with uv (used by "make start" above)
$. uv run fastapi dev main.py

# 2. Call fastapi directly with entry file:
$. fastapi dev main.py

# 3. Call fastapi directly without entry file (assumes it is "main.py")
$. fastapi dev
```

## Dependencies

Documentation links are provided for each dependency.

- [`uv`](https://docs.astral.sh/uv/): dependency and project manager.
- [GNU `make`](https://www.gnu.org/software/make/manual/make.html): For running makefiles.
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): for reading `.env` files in project
- [`fastapi`](https://fastapi.tiangolo.com/): a high performance API framework.
- [`py_webauthn`](https://pypi.org/project/webauthn/): Python3 server-side [WebAuthN API implementation](https://www.w3.org/TR/webauthn-2/). Enables passphrase authentication.
- [`prisma` (**Prisma Client Python**)](https://prisma-client-py.readthedocs.io/en/stable/): a Python port of a code-first ORM framework for NodeJS backends.
  - For the full API, visit the Prisma ORM docs [**here**](https://www.prisma.io/)

### What is uv?

[`uv`](https://docs.astral.sh/uv/) is a project and dependency manager. If you are familiar with NodeJS, it is somewhat similar to `npm`, in that you can use it to

- Initialize a project in a directory
- Install, review, and update project dependencies
- Create a dependency `.lock` file that freezes your dependency versions

### Adding dependencies with uv

You can use the following scripts to add, remove, or manage your dependencies:

- `uv add [dependency] [dependency] ...`: install new package(s) and update `project.toml`
- `uv remove [dependency]`: uninstall package
- `uv lock --upgrade`: **upgrade all packages** listed in `project.toml`
- `uv lock --upgrade [dependency]`: **upgrade a specified dependency** listed in `project.toml`

### Additional uv scripts

The following additional scripts help you run the project

- `uv run fastapi dev main.py`: run project
- `uv run [script]`: run any script in project context
- `uv build`: build a project bundle for distribution

## Troubleshooting

### Resolve dependency paths in VSCode

Worth noting, since I personally ran into this issue: if you are using VSCode, be sure to

- Open your command menu (**ctrl (or cmd for mac) + shift + p**),
- Search for and select the `Python: Select Interpreter` command, then
- Make sure it points to the virtual environment in the current directory (path begins with `.venv/...`)

This will ensure your workspace can correctly resolve dependencies.

### Silent migration failure when adding Enums

Database enums should not be created and applied as a default value in the same migration.

To avoid this:
  >
  > 1. Add your new enum (or enum property) and trigger migrations.
  > 2. Apply the new enum (or enum value) as a default column value, and trigger migrations again.
  >

You should also apply these steps to your production environment. This helps to prevent one source of silent migration failures.
