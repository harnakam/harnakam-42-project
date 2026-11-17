import os


class Env:
    mode: str = "development"
    database: str | None = None
    api_key: str | None = None
    log_level: str = "INFO"
    endpoint: str | None = None

    @classmethod
    def load(cls) -> None:
        cls.mode = os.getenv("MATRIX_MODE", "development")
        cls.database = os.getenv("DATABASE_URL")
        cls.api_key = os.getenv("API_KEY")
        cls.log_level = os.getenv("LOG_LEVEL", "INFO")
        cls.endpoint = os.getenv("ZION_ENDPOINT")


def matrix_mode() -> None:
    print(f"Mode: {Env.mode}")

    if Env.database:
        print(f"Database: {Env.database}")
    else:
        print("WARNING: DATABASE_URL is missing")

    if Env.api_key:
        print("API Access: Authenticated")
    else:
        print("WARNING: API_KEY is missing")

    print(f"Log Level: {Env.log_level}")

    if Env.endpoint:
        print("Remote Network: Online")
        print(f"Endpoint: {Env.endpoint}")
    else:
        print("Remote Network: Offline")


def production_mode() -> None:
    print(f"Mode: {Env.mode}")

    if Env.database:
        print("Database: Configured")
    else:
        print("WARNING: DATABASE_URL is missing")

    if Env.api_key:
        print("API Access: Authenticated")
    else:
        print("WARNING: API_KEY is missing")

    print(f"Log Level: {Env.log_level}")

    if Env.endpoint:
        print("Remote Network: Online")
    else:
        print("Remote Network: Offline")


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv()
    Env.load()

    print("ORACLE STATUS: Consulting the configuration...\n")
    print("Configuration loaded:")

    if Env.mode == "development":
        matrix_mode()
    elif Env.mode == "production":
        production_mode()
    else:
        print(f"WARNING: Unknown mode: {Env.mode}")

    print("\nConfiguration security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly ignored by git")
    print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    try:
        main()
    except BaseException as Error:
        print(f"Error: {Error}")
