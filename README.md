# pour

pour is an exceedingly simple, opinionated scaffolding tool for Flask 🍾

## Usage

### Creating an app

```bash
pour fresh <app>
```

This will initialize a new app with the following structure:

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

### Creating an empty feature slice

```bash
pour slice <name>
```

This will create three directories within the features directory:

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

This will scaffold a model, a controller, and a template that may be used for domain logic.
