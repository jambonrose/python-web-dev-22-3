# Read Me

This repository contains the code for the third class in [Andrew
Pinkham]'s [Python Web Development] series, titled *Advanced Web
Development in Python with Django*. The series is published by Pearson
and may be bought on [InformIT] or viewed on [Safari Books Online]. The
series is for intermediate programmers new to web development or Django.

[Andrew Pinkham]: https://andrewsforge.com
[Python Web Development]: https://pywebdev.com
[InformIT]: https://pywebdev.com/buy-22-3/
[Safari Books Online]: https://pywebdev.com/safari-22-3/

Andrew may be reached at [JamBon Software] for consulting and training.

[JamBon Software]: https://www.jambonsw.com

## Table of Contents

- [Changes Made Post-Recording](#changes-made-post-recording)
- [Technical Requirements](#technical-requirements)
- [Getting Started Instructions](#getting-started-instructions)
  - [Docker Setup](#docker-setup)
  - [Local Setup](#local-setup)
- [Walking the Repository](#walking-the-Repository)
- [Extra Problems](#extra-problems)
- [Testing the Code](#testing-the-code)
- [Deploying the Code](#deploying-the-code)

## Changes Made Post-Recording

1. The asynchronous code has been upgraded to work with Starlette 0.13
   and now works with ASGI 3.0

NB: The extra code for resizing images using Celery (mentioned in Lesson 6)
will be added in March 2020.

[🔝 Up to Table of Contents](#table-of-contents)

## Technical Requirements

- [Python] 3.6+ (with SQLite3 support)
- [pip] 19+
- a virtual environment (e.g.: [`venv`], [`virtualenvwrapper`])
- Optional:
  - [Docker] 17.12+ with [Docker-Compose] (or—if unavailable—[PostgreSQL] 10)


[Python]: https://www.python.org/downloads/
[pip]: https://pip.pypa.io/en/stable/installing/
[`venv`]:https://docs.python.org/3/library/venv.html
[`virtualenvwrapper`]: https://virtualenvwrapper.readthedocs.io/en/latest/install.html
[Docker]: https://www.docker.com/get-started
[Docker-Compose]: https://docs.docker.com/compose/
[PostgreSQL]: https://www.postgresql.org/

All other technical requirements are installed by `pip` using the
requirement files included in the repository. This includes [Django 2.2].

[Django 2.2]: https://docs.djangoproject.com/en/2.2/

[🔝 Up to Table of Contents](#table-of-contents)

## Getting Started Instructions

For a full guide to using this code please refer to Lesson 2 of the
second class. The lesson demonstrates how to get started locally as well
as how to use the Docker setup.

If you are **unable to run Docker** on your machine skip to the [Local
Setup](#local-setup) section.

### Docker Setup

The use of Docker images allows us to avoid installing all of our
dependencies—including PostgeSQL—locally. Furthermore, as discussed
in second class, it helps with parity between our development and
production environments.

Our Docker containers expect the existence of an environment file. To
generate it on *nix systems please invoke the `build_docker_env.sh`
script.

```shell
./build_docker_env.sh
```

On Windows please invoke the batch file.

```
build_docker_env
```

If you run into problems please refer to the videos for why we use this
and what is needed in the event these scripts do not work.

To run the Docker containers use the command below.

```shell
docker-compose up
```

If you wish to run the servers in the background use the `-d`
(**d**etached) flag, as demonstrated below.

```shell
docker-compose up -d
```

To turn off the server use Control-C in the terminal window. If running
in the background use the command below.

```shell
docker-compose down
```

To remove all of the assets created by Docker to run the server use the
command below.

```shell
docker-compose down --volumes --rmi local
```

The `--volumes` flag may be shortened to `-v`.

[🔝 Up to Table of Contents](#table-of-contents)

### Local Setup

Use `pip` to install your development dependencies.

```console
$ python3 -m pip install -r requirements/development.txt
```

If you have checked out to an earlier part of the code note that you
will need to use `requirements.txt` instead of
`requirements/development.txt`.

You will need to define the`SECRET_KEY` environment variable. If you
would like to use PostgreSQL locally you will need to set
`DATABASE_URL`.

```shell
export SECRET_KEY=`head -c 75 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 50`
# replace the variables in <> below
export DATABASE_URL='postgres://<USER>:<PASSWORD>@<SERVER>:5432/<DB_NAME>'
```

[🔝 Up to Table of Contents](#table-of-contents)

## Walking the Repository

To make perusing the code in this repository as simple as possible the
project defines its own `.gitconfig` file with custom commands
(aliases).

To enable the commands you must first point your local git
configuration at the file provided. Either of the two commands below
should work.

```shell
# relative path
git config --local include.path "../.gitconfig"
# absolute path - *nix only!
git config --local include.path "`builtin pwd`/.gitconfig"
```

This will enable the following git commands:

- `git next`: Move to the next example/commit
- `git prev`: Move to the previous example/commit
- `git ci`: shortcut for `git commit`
- `git co`: shortcut for `git checkout`
- `git st`: shortcut for `git status`
- `git ll`: shortcut for `git log --oneline`

These commands can be used on any of the branches in this
repository.

[🔝 Up to Table of Contents](#table-of-contents)
