import os

from app.core.config import settings


def get_absolute_path(project_path) -> str:
    return str(os.path.join(settings.PROJECT_DIR, project_path))


def get_resource(res_name: str):
    file_path = os.path.join(settings.PROJECT_DIR, "res", res_name)
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None
