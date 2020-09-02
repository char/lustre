# Comet

An opinionated, "batteries included" ASGI web framework on top of [Starlette](https://www.starlette.io/).

## Roadmap

- **Database support + ORM**
- Proper, `.env` and environment variable configuration (we get this for free with Starlette)
- 'Static fragments': Pre-computed (computed on-the-fly in development mode) blocks of data that we can include in templates, responses, or whatever - This lets us do expensive highlight.js syntax highlighting once at build time, and never again.
- We could extend the static fragments system to send whole computed static files.
- Proper, nice, logging support
