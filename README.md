# Lustre

An opinionated, "batteries included" ASGI web framework on top of [Starlette](https://www.starlette.io/) and the surrounding `encode.io` ecosystem.

Using Lustre will mainly entail:

- Writing `async` endpoint handlers.
- Writing templates using [Jinja](https://jinja.palletsprojects.com/).
- Accessing the database via encode's [`orm` module](https://github.com/encode/orm).

## Database Backends

Since we use encode's [`databases` module](https://www.encode.io/databases/), we support several database backends, but you will need to install the backing package separately:

- [SQLite](https://www.sqlite.org/), via `aiosqlite`.
- [PostgreSQL](https://www.postgresql.org/), via `aiopg`.
- [MySQL](https://www.mysql.com/) (and [MariaDB](https://mariadb.org/)) via `aiomysql`.

## Roadmap

- Proper, nice, logging support
- Potentially support 'freezing' a site into a static bundle - Pre-render templates, turn redirects into nginx configuration, et cetera.
