#! /usr/bin/env bash
alembic revision --autogenerate -m "Migration"
alembic upgrade head

