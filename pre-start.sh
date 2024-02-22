#! /usr/bin/env -S bash
alembic revision --autogenerate -m "Migration"
alembic upgrade head

