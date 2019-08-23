#/usr/bin/env sh

echo "REDIS_URL=redis://redis:6379
DEBUG=False
TESTING=False
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
" > .docker-env
