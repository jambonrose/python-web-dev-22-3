FROM revolutionsystems/python:3.7.2-wee-optimized-lto

WORKDIR /app

ENV PYTHONUNBUFFERED 1
RUN python3 -m pip install -U pip setuptools

COPY requirements /tmp/requirements
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc binutils libssl-dev \
    && python3 -m pip install -U --no-cache-dir \
        -r /tmp/requirements/base.txt \
        -r /tmp/requirements/development.txt \
    && DEBIAN_FRONTEND=noninteractive apt-get purge -y gcc binutils libssl-dev \
    && DEBIAN_FRONTEND=noninteractive apt-get -yq --purge autoremove \
    && find /var/lib/apt/lists \
        /usr/share/man \
        /usr/share/doc \
        /var/log \
        -type f -exec rm -f {} +

COPY docker/starlette/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
