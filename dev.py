r"""Dev Environment manager

This module starts up the dev (or prod) environment with a single command. 

When you run `dev.py --migrate`, it will apply any new `Prisma` migrations before 
re-starting the FastAPI server. This is necessary because 

1. `FastAPI` watches for changes in the project
2. The migration changes the `migrations/` directory, and so
3. `FastAPI` will fall into an endless loop when starting up.

So it is important to handle the migration squashing *before* FastAPI's lifecycle 
begins.

Migration files get squashed so that you are always left with a maximum of two SQL
files: one enables creation of the DB, and the second (if it exists) is a diff between
the "live" database and any new changes to the Prisma file. The `db_migrate` script can
be run in production, if you really don't care about lengthy migration histories.
"""

import argparse
import subprocess
import sys
import contextlib


# DB migration script (can be moved elsewhere )
from scripts.db_migrate import main as db_migrate


def start_server():
    """
    Starts the FastAPI server using `uv`
    """
    try:
        # subprocess.run(["uv", "run", "fastapi", "dev"], check=True)
        # subprocess.run(["uv", "run", "fastapi", "dev"])
        subprocess.run(["fastapi", "dev"])
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)


def start_environment(migrate=False):
    """
    Start dev environment with optional db squash-migration. When
    `--migrate` flag is included, will run `db_migrate` first.
    """

    print(f"Starting development environment with migration={migrate}")

    # sync db changes from schema.prisma and squash migrations
    if migrate:
        db_migrate()
        print("Db.Migrated")

    start_server()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        # Define CLI flags for starting environment
        parser = argparse.ArgumentParser(
            description="Start the development environment."
        )

        # "migrate" flag determines whether `db_migrate` runs first.
        parser.add_argument(
            "--migrate",
            action="store_true",
            help="Apply and squash db migrations before starting the dev environment",
        )

        # Get cli flags
        args = parser.parse_args()

        # Do what needs to be done
        start_environment(args.migrate)
