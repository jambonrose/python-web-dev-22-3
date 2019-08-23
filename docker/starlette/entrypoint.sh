#!/usr/bin/env sh

if [ "$#" = 0 ]
then
    python3 -m pip freeze
fi

if [ "$#" = 0 ]
then
    gunicorn -b 0.0.0.0:8000 -w 1 -k uvicorn.workers.UvicornWorker --log-level warning --chdir src starlette_totp_api.application:app
else
    >&2 echo "Command detected; running command"
    exec "$@"
fi
