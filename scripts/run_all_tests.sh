#!/bin/bash

poetry run pytest --cov=python_boilerplate tests

poetry run mypy python_boilerplate server --ignore-missing-imports
