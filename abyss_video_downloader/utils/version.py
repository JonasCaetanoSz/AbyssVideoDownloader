from pathlib import Path
import tomllib


def get_version():

    pyproject = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject, "rb") as file:
        data = tomllib.load(file)

    return data["project"]["version"]