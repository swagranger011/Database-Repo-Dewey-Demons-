# Database-Repo-Dewey-Demons

## Build Requirements

Strictly speaking, the only thing required to run this project is [docker](https://www.docker.com/).

Note the database runs at `localhost:6001`
This is different from the default `localhost:5432` to avoid conflicting with existing database (the default
postgres installs will start a service at 5432 which always runs to host a db)

```sh
docker-compose -f ./docker-compose.yml up --build
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

## Other Notes

- **Problem:** database in a bad state

  **Solution:** Simply delete all the data
  ```sh
  docker-compose -f ./docker-compose.yml down
  docker volume rm database-repo-dewey-demons_database
  ```