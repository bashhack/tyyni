#! /usr/bin/env bash

# Start the DB
python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data
python /app/app/initial_data.py
