#!/bin/bash

exec poetry run mypy python_boilerplate server --ignore-missing-imports
