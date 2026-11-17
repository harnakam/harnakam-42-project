import os
import site
import sys


class Envinfo:
    def __init__(self) -> None:
        self.is_virtual = self.is_virtual_env()

    def __repr__(self) -> str:
        return (
            f"===[INTERPRETER]===\n"
            f"Python: {sys.executable}\n"
            f"Version: {sys.version}\n"
            f"Details: {sys.version_info}\n"
            f"Implementation: {sys.implementation.name}\n"
            f"Platform: {sys.platform}\n"
            f"Prefix: {sys.prefix}\n"
            f"Base: {sys.base_prefix}\n"
            f"Import paths: {sys.path}\n"
            f"\n"
            f"===[ENVIRONMENT]===\n"
            f"Virtual: {self.is_virtual}\n"
            f"Virtual env: {os.getenv('VIRTUAL_ENV')}\n"
            f"Working directory: {os.getcwd()}\n"
            f"\n"
            f"===[PACKAGES]===\n"
            f"Site packages: {site.getsitepackages()}\n"
            f"User packages: {site.getusersitepackages()}\n"
            f"User site enabled: {site.ENABLE_USER_SITE}\n"
        )

    def __str__(self) -> str:
        if self.is_virtual:
            return (
                "LABORATORY STATUS: "
                "The laboratory is sealed\n"
                "\n"
                "Current Python: "
                f"{sys.executable}\n"
                "Virtual Environment: "
                f"{os.path.basename(sys.prefix)}\n"
                "Environment Path: "
                f"{sys.prefix}\n"
                "\n"
                "SUCCESS: You are working "
                "in an isolated environment!\n"
                "Safe to install reagents "
                "without affecting\n"
                "the global system.\n"
                "\n"
                "Reagent installation path:\n"
                + "\n".join(site.getsitepackages())
                + "\n\nGlobal reagent installation paths:\n"
                + "\n".join(site.getsitepackages([sys.base_prefix]))
            )
        return (
            "LABORATORY STATUS: "
            "You are working in the open\n"
            "\n"
            "Current Python: "
            f"{sys.executable}\n"
            "Virtual Environment: "
            "None Detected\n"
            "\n"
            "WARNING: "
            "You are in the global environment!\n"
            "Every reagent you install here leaks "
            "into the whole system.\n"
            "\n"
            "To seal the laboratory, run:\n"
            "python3 -m venv lab_env\n"
            "source lab_env/bin/activate # On Unix\n"
            "lab_env\\Scripts\\activate # On Windows\n"
            "\n"
            "Then run this program again.\n"
            "\n"
            "Global reagent installation paths:\n"
            + "\n".join(site.getsitepackages([sys.base_prefix]))
            + "\n\nVirtual environment packages are stored under "
            "lab_env, separately from these global paths."
        )

    @staticmethod
    def is_virtual_env() -> bool:
        return sys.prefix != sys.base_prefix


def main() -> None:
    env = Envinfo()
    if "--dev" in sys.argv[1:]:
        print(repr(env))
    else:
        print(env)


if __name__ == "__main__":
    main()
