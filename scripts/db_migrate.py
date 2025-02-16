#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import subprocess
import shutil
import uuid
from pathlib import Path


# Access environment variables
load_dotenv()

# Define paths
script_dir = Path(__file__).resolve().parent
migrations_path = (script_dir / "../prisma/migrations").resolve()
squashed_migrations = migrations_path / "000000000000_squashed_migrations"
squashed_diff = migrations_path / f"{uuid.uuid4()}_squashed_diff"

# Get the short DB URL from the environment variable DB_URL
db_url = os.environ.get("DB_URL")
short_db_url = db_url.split("?")[0] if db_url else None


def generate_client():
    if not short_db_url:
        print("Error: Missing database URL")
        return
    try:
        output = subprocess.check_output(["prisma", "generate"])
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print("Error generating client:", e)


def clear_past_migrations():
    if not short_db_url:
        print("Error: Missing database URL")
        return
    try:
        if migrations_path.exists():
            shutil.rmtree(migrations_path, ignore_errors=True)
    except Exception as e:
        print("Error clearing past migrations:", e)


def make_squashed_migration():
    if not short_db_url:
        print("Error: Missing database URL")
        return
    try:
        # Ensure the squashed migration directory exists
        squashed_migrations.mkdir(parents=True, exist_ok=True)
        # Generate a full migration script from an empty database state to the current schema
        squashed_migration = subprocess.check_output(
            [
                "prisma",
                "migrate",
                "diff",
                "--from-empty",
                "--to-schema-datamodel",
                "./prisma/schema.prisma",
                "--script",
            ]
        )
        migration_sql_path = squashed_migrations / "migration.sql"
        with open(migration_sql_path, "wb") as f:
            f.write(squashed_migration)
        # Mark the squashed migration as applied
        prisma_out = subprocess.check_output(
            [
                "prisma",
                "migrate",
                "resolve",
                "--applied",
                str(squashed_migrations),
            ]
        )
        print(prisma_out.decode())
    except subprocess.CalledProcessError as e:
        print("Error in making squashed migration:", e)


def make_squashed_diff():
    if not short_db_url:
        print("Error: Missing database URL")
        return
    try:
        # Create a unique directory for the differential migration
        squashed_diff.mkdir(parents=True, exist_ok=True)
        squashed_diff_migration = subprocess.check_output(
            [
                "prisma",
                "migrate",
                "diff",
                "--from-url",
                short_db_url,
                "--to-schema-datamodel",
                "./prisma/schema.prisma",
                "--script",
            ]
        )
        migration_sql_path = squashed_diff / "migration.sql"
        with open(migration_sql_path, "wb") as f:
            f.write(squashed_diff_migration)
        print("squashedDiffMigration:")
        print(squashed_diff_migration.decode())
    except subprocess.CalledProcessError as e:
        print("Error in making squashed diff migration:", e)


def deploy_migration():
    if not short_db_url:
        print("Error: Missing database URL")
        return
    try:
        prisma_out = subprocess.check_output(["prisma", "migrate", "deploy"])
        print(prisma_out.decode())
    except subprocess.CalledProcessError as e:
        print("Error deploying migration:", e)


def main():
    if not short_db_url:
        print("Error: Missing database URL")
        return
    try:
        print("Starting db migration:")
        generate_client()
        clear_past_migrations()
        make_squashed_migration()
        make_squashed_diff()
        deploy_migration()
    except Exception as e:
        print("DB Migrate failed:", e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", e)
