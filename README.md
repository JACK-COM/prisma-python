# Prisma Python

A project template for a Python-backend API. Uses **Prisma**, **FastAPI**, **DotEnv**, and **WebAuthN**, with **uv** for project and dependency management.\
See [dependencies](#dependencies) for the list, as well as documentation links.

The repository is similar to [JACK-COM's prisma-express](https://github.com/JACK-COM/prisma-express) starter template for NodeJS projects. It is also heavily inspired by the [prisma-korea/prisma-fastapi](https://github.com/prisma-korea/prisma-fastapi/tree/main) repository, and uses some of the latter's directory structures and starter files while simplifying dependency management.

If you are familiar with any of the [dependencies](#dependencies) and/or Python, it should be straightforward to use.

## Table of Contents

- [Prisma Python](#prisma-python)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Before you start](#before-you-start)
  - [Development](#development)
    - [1. Install project dependencies with uv](#1-install-project-dependencies-with-uv)
    - [2. Run the project](#2-run-the-project)
      - [Development Environment](#development-environment)
      - [Table Changes and Database Migrations](#table-changes-and-database-migrations)
      - [Run API without prisma migrations](#run-api-without-prisma-migrations)
        - [1. call fastapi with uv](#1-call-fastapi-with-uv)
        - [2. run fastapi with or without main filename](#2-run-fastapi-with-or-without-main-filename)
  - [Dependencies](#dependencies)
    - [What is uv?](#what-is-uv)
    - [Adding dependencies with uv](#adding-dependencies-with-uv)
    - [Additional uv scripts](#additional-uv-scripts)
  - [Troubleshooting](#troubleshooting)
    - [Resolve dependency paths in VSCode](#resolve-dependency-paths-in-vscode)
    - [Silent migration failure when adding Enums](#silent-migration-failure-when-adding-enums)

## Getting Started

### Before you start

This is only needed for setting things up after you first clone the project. I promise it is faster than it looks.

At a high level, you will need to take these steps [(**details here**)](./PRE_SETUP.md).

1. Install `uv` globally (see [dependencies](#dependencies)) for working with dependencies.
2. Create a database with your preferred provider. Prisma supports the popular ones (`postgres`, `mongo`, and `sqlite`)
3. Configure your `.env` file with a path to the new database. The setup document will show the correct format for postgres databases; visit the [Prisma docs](https://www.prisma.io/) to get the syntax for other providers.
4. (Optional) modify the `schema.prisma` file to reflect the database you want.

Detailed instructions are [**here**](./PRE_SETUP.md).\
Once you have your database and `.env` file configured, and have installed `uv`, you can continue with the steps below.

## Development

### 1. Install project dependencies with uv

This part should be familiar if you're coming from a JS/TS/NPM background.

Run the following in the project root (where `pyproject.toml` can be found). This will install project dependencies specified in the included `uv.lock` file. See [additional scripts](#additional-uv-scripts) for commands to update one or more dependencies.

```bash
$. uv pip install -r pyproject.toml
```

### 2. Run the project

#### Development Environment

Run the following in the project root (where `pyproject.toml` can be found).\
This will run the application in dev mode.

```bash
$. uv run dev.py
```

`dev.py` accepts an optional `--migrate` boolean flag. When present, it will trigger a prisma migration to sync your db with the `schema.prisma` file before starting up. See [Table Changes](#table-changes-and-database-migrations) below.

#### Table Changes and Database Migrations

To add (or change) your database:

1. Modify the `schema.prisma` file (add tables/columns/etc) and save your changes
2. Restart the app and include the `--migrate` flag to apply changes to the database before the server starts up.

```bash
$. uv run dev.py --migrate
```

This allows you to sync your changes by simply re-starting the dev server.

#### Run API without prisma migrations

If you don't care at all about using prisma the migration script, use any of the following to start the project:

##### 1. call fastapi with uv

```bash
$. uv run fastapi dev main.py
```

##### 2. run fastapi with or without main filename

```bash
# Option 1
$. fastapi dev main.py

# Option 2
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
- [`bump-my-version`](https://callowayproject.github.io/bump-my-version/): semantic project version bumping with `make`
- [`git-changelog`](https://pypi.org/project/git-changelog/): for generating project release changelogs.

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
