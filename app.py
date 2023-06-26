import os
import re
import platform
import subprocess
from typing import List

import click
import jinja2


def poetry(command: str, *args: str) -> subprocess.Popen:
    return subprocess.Popen(
        ["poetry", command] + list(args),
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def poetry_init() -> None:
    click.echo("⏳ Configuring project...")

    p: subprocess.Popen = poetry("init")

    def write(s: str) -> None:
        p.stdin.write(s)
        p.stdin.flush()

    # Confirm metadata
    for _ in range(6):
        write(b"\n")

    # Skip dependencies
    write(b"no\n")
    write(b"no\n")

    # Confirm generation
    write(b"\n")
    p.wait()

    def add_package(package: str) -> None:
        poetry("add", package).wait()
        click.echo(f"\t✅ Added {package}")

    add_package("flask")
    add_package("Flask-SQLAlchemy")
    add_package("python-dotenv")
    add_package("gunicorn")

    poetry("add", "--group", "dev", "black").wait()
    click.echo("\t✅ Added black")

    poetry("install").wait()
    click.echo("\t✅ Resolved dependencies")
    click.echo("")


def scaffold_app(name: str) -> None:
    destination: str = os.path.join(os.getcwd(), name)
    if os.path.exists(destination):
        raise click.ClickException(
            f'Cannot pour "{name}" into existing directory ({destination}).'
        )

    click.echo(f'🫗 Pouring "{name}"')
    click.echo("")

    os.mkdir(destination)
    os.chdir(destination)

    poetry_init()

    click.echo("⏳ Scaffolding app...")

    templates = "../template/app"
    for root, dirs, files in os.walk(templates):
        relative_path = os.path.relpath(root, templates)
        destination_dir = os.path.join(destination, relative_path)
        os.makedirs(destination_dir, exist_ok=True)

        for file in files:
            with open(os.path.join(root, file), "r") as f:
                contents: str = f.read()

            with open(os.path.join(destination_dir, file), "w") as f:
                template = jinja2.Template(contents)
                contents = template.render(name=name, python_version=platform.python_version())

                f.write(contents)
                click.echo(f"\t✅ {file}")


@click.command()
@click.argument("name")
def fresh(name: str) -> None:
    if not re.match(r"^[a-zA-Z0-9_]+$", name):
        raise click.BadParameter(
            "Name must be a valid Python module name. Please use only letters, numbers, and underscores."
        )

    scaffold_app(name)


def scaffold_slice(name: str) -> None:
    path: str = os.path.join(os.getcwd(), "app/features", name)
    if os.path.exists(path):
        raise click.ClickException(f'Cannot slice "{name}" as it already exists.')

    click.echo(f'🫗 Adding slice "{name}"')

    os.makedirs(path)
    os.chdir(path)

    os.mkdir("routes")
    os.mkdir("models")
    os.mkdir("domain")

    click.echo("")


@click.command()
@click.argument("name")
def slice(name: str) -> None:
    if not re.match(r"^[a-z0-9_]+$", name):
        raise click.BadParameter(
            "Name must be a valid Python module name. Please use only lowercase letters, numbers, and underscores."
        )

    scaffold_slice(name)


def scaffold_ingredient(slice: str, ingredient: str, cols: List[str]) -> None:
    click.echo(f'⏳ Adding "{ingredient}"')

    camel_case_ingredient = "".join(
        [word.capitalize() for word in ingredient.split("_")]
    )

    hint_to_type = {
        "int": "Integer",
        "float": "Float",
        "str": "String",
        "bool": "Boolean",
        "datetime": "DateTime",
    }
    mapped_cols = []
    for col in cols:
        name, type = col.split(":")
        mapped_cols.append((name, hint_to_type[type]))

    templates = os.path.abspath("../template/ingredient")
    with open(os.path.join(templates, "model.py"), "r") as f:
        contents: str = f.read()

    path: str = os.path.join(os.getcwd(), "app/features", slice)
    with open(os.path.join(path, "models", f"{ingredient}.py"), "w") as f:
        template = jinja2.Template(contents)

        contents = template.render(
            name=ingredient,
            name_camel=camel_case_ingredient,
            cols=mapped_cols,
        )

        f.write(contents)
        click.echo(f"\t✅ {ingredient}.py")

    with open(os.path.join(templates, "route.py"), "r") as f:
        contents: str = f.read()

    with open(os.path.join(path, "routes", f"{ingredient}.py"), "w") as f:
        template = jinja2.Template(contents)
        contents = template.render(feature=slice, name=ingredient)

        f.write(contents)
        click.echo(f"\t✅ {ingredient}.py")

    with open(os.path.join(templates, "service.py"), "r") as f:
        contents: str = f.read()

    with open(os.path.join(path, "domain", f"{ingredient}_service.py"), "w") as f:
        template = jinja2.Template(contents)
        contents = template.render(
            feature=slice, name=ingredient, name_camel=camel_case_ingredient
        )

        f.write(contents)
        click.echo(f"\t✅ {ingredient}_service.py")


@click.command()
@click.argument("ingredient")
@click.argument("slice")
@click.option("--col", multiple=True, help="Specify a column for the model")
def ingredient(ingredient: str, slice: str, col: List[str]) -> None:
    if not re.match(r"^[a-z0-9_]+$", slice):
        raise click.BadParameter(
            "slice must be a valid Python module name. Please use only lowercase letters, numbers, and underscores."
        )

    if not re.match(r"^[a-z0-9_]+$", ingredient):
        raise click.BadParameter(
            "Ingredient must be a valid Python module name. Please use only lowercase letters, numbers, and underscores."
        )

    if not os.path.exists(os.path.join(os.getcwd(), "app/features", slice)):
        raise click.BadParameter(
            f'slice "{slice}" does not exist. Please create the slice first.'
        )

    scaffold_ingredient(slice, ingredient, col)


@click.group()
def cli():
    pass


cli.add_command(fresh)
cli.add_command(slice)
cli.add_command(ingredient)

if __name__ == "__main__":
    cli()
