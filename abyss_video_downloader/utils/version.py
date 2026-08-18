from pathlib import Path
import re

def _get_version_from_pyproject(start=None):
    start_path = Path(start) if start else Path(__file__).resolve()
    for parent in (start_path, *start_path.parents):
        pyproject = parent / "pyproject.toml"
        if not pyproject.exists():
            continue
        try:
            try:
                import tomllib as toml
                with pyproject.open("rb") as f:
                    data = toml.load(f)
            except Exception:
                import tomli as toml
                with pyproject.open("rb") as f:
                    data = toml.load(f)
            version = None
            if isinstance(data, dict):
                project = data.get("project")
                if isinstance(project, dict):
                    version = project.get("version")
                if not version:
                    tool = data.get("tool", {})
                    poetry = tool.get("poetry") if isinstance(tool, dict) else None
                    if isinstance(poetry, dict):
                        version = poetry.get("version")
            if version:
                return str(version)
        except Exception:
            try:
                text = pyproject.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r'^\s*version\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
                if m:
                    return m.group(1)
            except Exception:
                pass
    return None

def get_version() -> str:
    v = _get_version_from_pyproject()
    return v if v else "unknown"
