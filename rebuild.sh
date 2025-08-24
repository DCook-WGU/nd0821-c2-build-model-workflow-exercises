#!/bin/bash

# Make script strict. Will not fail silently. 
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-mlops-course}"
IMAGE="${IMAGE:-mlops-dev-course}"

echo "Stopping/removing old container (if any): $CONTAINER_NAME"
docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
docker rm   "$CONTAINER_NAME" >/dev/null 2>&1 || true

echo "Building image: $IMAGE"
# If your Dockerfile supports build args (ENV_NAME, etc.), pass them here:
# docker build --build-arg ENV_NAME=mlops --build-arg ENV_FILE=/app/environment.yml -t "$IMAGE" .
# docker build -t "$IMAGE" .


NO_CACHE=${NO_CACHE:-0}
[[ "$NO_CACHE" == "1" ]] && NC_FLAG="--no-cache" || NC_FLAG=""
docker build --pull -t "$IMAGE" .

echo "Rebuilt image: $IMAGE"

# To run no cache rebuild, use command below.
# NO_CACHE=1 ./rebuild.sh


# Original Version

#!/bin/bash
#docker stop mlops-container && docker rm mlops-container
#docker build -t mlops-dev .
