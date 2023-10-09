# {{ name }}

This is a Flask project bootstrapped with [`pour`](https://github.com/dkgv/pour).

## Usage

Run the development server:

```bash
python wsgi.py
```

Manage dependencies with `poetry`:

```bash
poetry add <package>
```

Generate database migrations with `alembic` through `Flask-Migrate`:
```bash
flask db migrate -m "message"
```

These are automatically applied when running your app.
