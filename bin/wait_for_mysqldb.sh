#!/bin/sh

python3 -m app.wait_for_mysql

exec "$@"
