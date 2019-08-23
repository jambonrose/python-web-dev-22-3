#!/bin/sh

set -o errexit
set -o nounset


rm -f './celerybeat.pid'
celery -A config beat -l INFO
