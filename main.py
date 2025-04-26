from dotenv import load_dotenv
from src.migrations import run_migrations
load_dotenv()

from src.seed import seed_database # noqa: E402


def main():
    print("Running migrations")
    run_migrations()
    print("Migrations complete")

    print("Seeding database")
    seed_database()
    print("Seeding complete")


if __name__ == "__main__":
    main()
