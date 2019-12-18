#! /usr/bin/env bash

# Start the DB
python /app/app/backend_pre_start.py

# Run DB migrations
alembic upgrade head