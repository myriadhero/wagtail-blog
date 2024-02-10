#! /usr/bin/bash
# this script should check if new version of the project is available on git
# and rebuild containers if so

git remote update

if git status -uno | grep "Your branch is behind 'origin/main'"; then
    # 1. pull the new version
    git pull

    # 2. build new docker containers
    docker compose --profile prod build

    # 3. restart the containers
    docker compose --profile prod up -d

    # 4. run migrate and collectstatic commands
    docker compose --profile prod exec web python manage.py migrate --noinput
    docker compose --profile prod exec web python manage.py collectstatic --noinput

    # 5. restart the web container
    docker compose --profile prod restart web
fi
