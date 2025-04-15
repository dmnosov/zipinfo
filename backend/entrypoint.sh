#!/bin/bash
set -e
poetry run alembic upgrade head
poetry run python -m main