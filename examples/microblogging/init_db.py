#!/usr/bin/env python3

from run_dev import random_secret_key

random_secret_key()

from microblogging import app, DATABASE_URL
from sqlalchemy import create_engine

if __name__ == "__main__":
    app.db.metadata.create_all(create_engine(str(DATABASE_URL)))
