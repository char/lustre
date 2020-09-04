# An alembic script designed to sit at migrations/env.py
#
# Update the referenced package in the 'Application' section.
#
# ============
# Housekeeping
# ============

import os.path
import sys

parent_path = os.path.abspath(os.path.join(__file__, "../../"))
sys.path.insert(0, parent_path)

from alembic import context
from logging.config import fileConfig

fileConfig(context.config.config_file_name)

# ===========
# Application
# ===========

from comet.ext.alembic import setup_alembic
from my_webapp import app

setup_alembic(app, context)
