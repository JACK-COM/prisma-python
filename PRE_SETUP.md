# Before you start

The following instructions should prepare you to get started with this project for the first time. You only need to performe them once. The first two steps can be performed in any order, since they are independent of each other.

## Table of Contents

- [Before you start](#before-you-start)
  - [Table of Contents](#table-of-contents)
  - [1. Create a database](#1-create-a-database)
  - [2. Install uv](#2-install-uv)
  - [3. Update your ENV file](#3-update-your-env-file)
    - [A note on environment variables](#a-note-on-environment-variables)
    - [A note on database providers](#a-note-on-database-providers)
  - [4. Check your schema file](#4-check-your-schema-file)
    - [Updating your database schema](#updating-your-database-schema)

## 1. Create a database

> **Prisma** operates against a target database, which must be present before running any `prisma` commands. Prisma also supports `mysql`, `sqlite`, `sqlserver` and `mongodb`. If you have a preferred (and empty) DB for testing, you can skip these instructions and move on to the next section.

First, create a database using one of Prisma's [supported providers](https://www.prisma.io/docs/pulse#supported-databases-and-providers).\
If you are using `postgresql`, you can use the [`psql`](https://www.postgresguide.com/utilities/psql/) utility to do it with the following steps:

```bash
# Log into your postgres instance as user "postgres" or your preferred superuser:
$. psql -U postgres

# Create the database (replace "DATABASE_NAME" with the name of the new database):
$. create database DATABASE_NAME;

# You can disconnect once you see the "create DATABASE" confirmation output with:
$. \q
```

Once you have a database, follow the next steps.

## 2. Install uv

Install [`uv`](https://docs.astral.sh/uv/) globally if you don't already have it installed.

## 3. Update your ENV file

1. **Create your `.env` file:** The repo includes an `env.sample` file, which you can copy to a new `.env` file, or simply rename to `.env`.
2. Point the `DB_URL` variable in your `.env` file to your new database.
   1. The path should reflect your [database provider](#a-note-on-database-providers) (see [Prisma docs](https://www.prisma.io/docs/pulse#supported-databases-and-providers)).
   2. If the database requires a specific `username` & `password` combination, replace the corresponding strings in the `DB_URL` variable below.
   3. Your end result should look something like this (configured for postgres), where `DATABASE_NAME` is the name of your new database:

   ```dotenv
   DB_URL="postgresql://username:password@localhost:5432/DATABASE_NAME"
   ```

### A note on environment variables

You can change `DB_URL` to any key you prefer (`SUPER_SECRET_DB`, for example). If you *do* change this value, make sure you change the reference in both the **db_migrate.py** script, as well as the **schema.prisma** file.

### A note on database providers

> **If you aren't using `postgresql`**, update the `provider` of the `datasource` block in schema.prisma to match your database provider. Remember Prisma also supports `mysql`, `sqlite`, `sqlserver` and `mongodb`.

Now let's get inside the python project.

## 4. Check your schema file

   The [included `schema.prisma` file](./prisma/schema.prisma) contains model definitions for a `Users` table, as well as a `Profile` and `Post` table. You can alter the file as needed.\
   Take care of this part before syncing the database.

### Updating your database schema

   > The `schema.prisma` file can be changed often. However, breaking changes may wipe your seed data if you use `prisma db push`, so this is a good time to be reckless.

And now you're MOAR REDDY to get started.

Return to [the main README](./README.md#development) to get you some dependencies.
