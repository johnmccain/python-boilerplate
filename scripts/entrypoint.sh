#!/bin/bash

# Use the host and port from the dynaconf configuration
HOST=$(python -c "from python_boilerplate.config.config import config; print(config['app.host'])")
PORT=$(python -c "from python_boilerplate.config.config import config; print(config['app.port'])")

exec uvicorn server.main:app --host $HOST --port $PORT
