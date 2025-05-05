# Database-Repo-Dewey-Demons

## Build Requirements

Strictly speaking, the only thing required to run this project is [docker](https://www.docker.com/).

You'll need to fill out the `.env`

```sh
cp .env-SAMPLE .env
vim .env # or use your preferred code editor
```

Then start Docker

This will start the database, run migrations (ie. create logical relations), and seed some starting data.

```sh
docker-compose -f ./docker-compose.yml up --build
```

Then in a _different_ terminal window run:

```sh
docker-compose exec db bash # or a shell of your choice
```

You can connect manually with (assuming you have postgresql tooling installed)

```sh
psql -U username -p 6001 -d eecs447
```

or

```sh
psql -U username -p 5432 -d eecs447
```

## Development Requirements

Only needed if developing or working on the databases.

**Required**:

- [docker](https://www.docker.com/)
- [uv](https://github.com/astral-sh/uv)
  > An extremely fast Python package and project manager
- python 3.12

**Optional**

A python version manager is generally recommended

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-win](https://github.com/pyenv-win/pyenv-win)

Strictly speaking, postgresql is not needed locally since docker will host our
database image to avoid any local database conflicts. But may be a helpful
install

- [postgresql](https://www.postgresql.org/)
  - [pgadmin](https://www.pgadmin.org/), prompted as an additional
    tool you can install when installing postgres, useful for viewing and connecting to a postgres database.

## Getting started

You'll need to fill out the `.env`

```sh
cp .env-SAMPLE .env
vim .env # or use your preferred code editor
```

**Installing python deps**

```sh
uv sync
```

- You then can use this virtual environment in your IDE/code editor
  - in vscode
    1. Open command palette `CTRL`+`SHIFT`+`P`
    2. Type `Python: Select Interpreter`
    3. Input the `.venv` path, typically at `.venv/Scripts/python.exe`

**Generating a new migration**

```sh
uvx alembic revision -m "i am adding tables and shi"
```

## Other Notes

- **Problem:** database in a bad state

  **Solution:** Simply delete all the data

  ```sh
  docker-compose -f ./docker-compose.yml down
  docker volume rm database-repo-dewey-demons_database
  ```
