from dotenv import load_dotenv
from src.migrations import run_migrations
from sqlalchemy import create_engine

load_dotenv()

def main():
    print("Hello from database-repo-dewey-demons!")


if __name__ == "__main__":
    main()
    run_migrations()

    # engine = create_engine("postgresql://username:password@localhost:6001/eecs582")
    # conn = engine.connect()
    # print("Connection successful!")
    # conn.close()
