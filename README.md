# pour

pour is an exceedingly simple, opinionated scaffolding tool for Flask 🍾

## Usage

### Creating an app

```bash
pour new <app>
```

This initializes a new app with the following structure:

```
<app>/
    app/
        __init__.py
        blueprints.py
        database.py
    .env
    poetry.lock
    poetry.toml
    README.md
    wsgi.py
```

Run the app by entering the Poetry environment with `poetry shell` and running `python wsgi.py`.

### Creating an empty feature slice

```bash
pour slice <name>
```

This creates three directories within the features directory:

```
<app>/
    app/
        features/
            <name>/
                domain/
                models/
                routes/
        [...]
    [...]
```

### Scaffolding a feature slice

```bash
pour ingredient <ingredient> <feature> --col <column_name1>:<column_type> --col <column_name2>:<column_type>
```

This defines a database model + database migration, a controller, and a template for domain logic. The model includes `id`, `created_at`, and `updated_at` columns by default.

Shorthand Python syntax can be used for the following column data types: `int`, `float`, `str`, `bool`, and `datetime`. All other data types must follow the naming specified by SQLAlchemy [here](https://docs.sqlalchemy.org/en/20/core/types.html).
