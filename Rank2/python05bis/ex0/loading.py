import importlib


def check_package(name: str) -> str:
    try:
        module = importlib.import_module(name)
        version = module.__version__
        return f"[OK] {name} {version}"
    except ImportError:
        return f"[MISSING] {name}"


def main() -> None:
    print("REAGENT STATUS: Loading reagents...")
    print("\nChecking dependencies:\n")

    for name in ("numpy", "pandas"):
        print(check_package(name))

    print("\nInstallation commands:")
    print("pip install -r ex0/requirements.txt")
    print("cd ex0 && poetry install")
    print("\npip vs Poetry:")
    print("pip installs packages from requirements.txt.")
    print("Poetry manages dependencies using pyproject.toml.")
    print("Poetry locks resolved versions in poetry.lock.")


if __name__ == "__main__":
    main()
