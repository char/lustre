#!/usr/bin/env python3

import uvicorn


def random_secret_key():
    import os

    os.environ.setdefault("SESSION_SECRET_KEY", os.urandom(32).hex())


if __name__ == "__main__":
    random_secret_key()
    uvicorn.run("microblogging:app", host="127.0.0.1", port=5000, reload=True)
