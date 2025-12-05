#!/bin/sh

# Stop on error
set -e

echo "Starting deployment script..."

# Run database migrations
# This ensures the tables exist in Postgres before the app starts
echo "Running database migrations..."
alembic upgrade head

# Start the application
# Host 0.0.0.0 is crucial for Docker to expose the port
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 3000