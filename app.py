import os
import platform
import re
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
    click.echo("⏳ Resolving dependencies")

    p: subprocess.Popen = poetry("init")

    def write(s: bytes) -> None:
        if not p.stdin:
            raise Exception("No stdin, cannot initialize project")

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
        click.echo(f"\t✅ Installed `{package}`")

    add_package("flask")
    add_package("Flask-SQLAlchemy")
    add_package("Flask-Migrate")
    add_package("python-dotenv")
    add_package("gunicorn")
    add_package("psycopg2")

    poetry("add", "--group", "dev", "black").wait()
    click.echo("\t✅ Installed `black`\n")

    poetry("install").wait()

    click.echo("⏳ Initializing git repository")
    subprocess.Popen(["git", "init"], stdout=subprocess.DEVNULL).wait()

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

    click.echo("⏳ Scaffolding app")

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
                contents = template.render(
                    name=name, python_version=platform.python_version()
                )

                f.write(contents)
                click.echo(f"\t✅ {file}")

    click.echo("")


@click.command()
@click.argument("name")
def new(name: str) -> None:
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
    mapped_cols = [
        (name, hint_to_type[type]) for col in cols for name, type in [col.split(":")]
    ]

    templates = os.path.abspath("../template/ingredient")

    def write_file(template_name: str, output_name: str, **kwargs):
        with open(os.path.join(templates, template_name), "r") as f:
            contents: str = f.read()

        path: str = os.path.join(os.getcwd(), "app/features", slice)
        with open(os.path.join(path, output_name), "w") as f:
            template = jinja2.Template(contents)

            contents = template.render(**kwargs)

            f.write(contents)
            click.echo(f"\t✅ {output_name}")

    write_file(
        "model.py",
        os.path.join("models", f"{ingredient}.py"),
        name=ingredient,
        name_camel=camel_case_ingredient,
        cols=mapped_cols,
    )

    write_file(
        "route.py",
        os.path.join("routes", f"{ingredient}.py"),
        feature=slice,
        name=ingredient,
    )

    write_file(
        "service.py",
        os.path.join("domain", f"{ingredient}_service.py"),
        feature=slice,
        name=ingredient,
        name_camel=camel_case_ingredient,
    )


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


def main():
    cli.add_command(new)
    cli.add_command(slice)
    cli.add_command(ingredient)
    cli()


if __name__ == "__main__":
    main()
