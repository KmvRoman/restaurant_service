#!/bin/bash

alembic upgrade head
python web.py &
python bot.py &

wait -n

exit $?
