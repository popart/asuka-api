# building
Run /scripts/download_models.py to fetch models
Build in an AL2023 VM (since that's what we're deploying to)

# docker build for local test
docker buildx build -t asuka-api:dev .
docker run -it -p 5000:5000 asuka-api:dev /bin/bash

# docker build for deploy
docker buildx build  --platform linux/amd64 -t us-docker.pkg.dev/kyoshi-dev/asuka/asuka-api:dev .
