@echo off

set PG_DB=webdev22videos3
set PG_PASSWORD=%RANDOM%%RANDOM%%RANDOM%
set PG_SERVICE_NAME=postgres
set PG_USER=webdev22videos3_user
set SKEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%

Echo POSTGRES_DB=%PG_DB% > .docker-env
Echo POSTGRES_PASSWORD=%PG_PASSWORD% >> .docker-env
Echo POSTGRES_USER=%PG_USER% >> .docker-env
Echo DATABASE_URL=postgres://%PG_USER%:%PG_PASSWORD%@%PG_SERVICE_NAME%:5432/%PG_DB% >> .docker-env
Echo MEMCACHE_URL=pymemcache://memcached:11211 >> .docker-env
Echo SECRET_KEY=%SKEY% >> .docker-env
