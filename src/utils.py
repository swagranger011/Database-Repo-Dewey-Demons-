import os


def get_url() -> str:
    username = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    in_docker = os.environ.get("DOCKER")

    if not username:
        raise ValueError(
            "POSTGRES_USER environment variable not set.",
            "Please ensure you have a .env file with POSTGRES_USER defined.",
        )

    if not password:
        raise ValueError(
            "POSTGRES_PASSWORD environment variable not set.",
            "Please ensure you have a .env file with POSTGRES_PASSWORD defined.",
        )

    if in_docker:
        return f"postgresql+psycopg2://{username}:{password}@db:5432/eecs447"

    return f"postgresql+psycopg2://{username}:{password}@localhost:6001/eecs447"
