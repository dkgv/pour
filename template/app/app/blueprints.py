import os
import runpy

from flask import Blueprint, Flask


def register_blueprints(app: Flask) -> None:
    for dir_name, _, file_names in os.walk("app/features"):
        for file_name in file_names:
            if not file_name.endswith(".py") or "models" in dir_name:
                continue

            module_path = os.path.join(dir_name, file_name)
            try:
                module_dict = runpy.run_path(module_path)
                for element in module_dict.values():
                    if isinstance(element, Blueprint):
                        app.register_blueprint(element)
            except Exception as e:
                print(f"Failed to process {module_path}: {str(e)}")
