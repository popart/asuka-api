# building
Run /scripts/download_models.py to fetch models
Build in an AL2023 VM (since that's what we're deploying to)

# docker build for local test
```
docker buildx build -t asuka-api:dev .
docker run -it -p 5000:5000 asuka-api:dev /bin/bash
```

# docker build for deploy
```
docker buildx build  --platform linux/amd64 -t us-docker.pkg.dev/kyoshi-dev/asuka/asuka-api:dev .
```

# deploy
```
gcloud auth application-default login
gcloud auth login
docker push us-docker.pkg.dev/kyoshi-dev/asuka/asuka-api:dev
```
(see https://cloud.google.com/artifact-registry/docs/docker/authentication if problems)

in cloud run console, deploy the new image as an updated revision
(make sure all the secrets are referenced)

