"""Configuration of the app"""
from starlette.config import Config
from starlette.datastructures import (
    URL,
    CommaSeparatedStrings,
)

# Reads environment variables and/or ".env" files
config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
REDIS_URL = config("REDIS_URL", cast=URL)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)
