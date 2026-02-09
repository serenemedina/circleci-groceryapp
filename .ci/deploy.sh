#!/bin/bash

# This script triggers a Render deploy hook and verifies the deployment
# actually succeeded by checking the HTTP response status

# Docker image details are passed in as arguments
IMAGE_REGISTRY="${1}"
IMAGE_NAMESPACE="${2}"
IMAGE_NAME="${3}"
IMAGE_TAG="${4}"

# Fail fast if required arguments are not given, exit CI immediately
if [[ $# -eq 0 ]]; then
  echo "usage: deploy.sh IMAGE_REGISTRY IMAGE_NAMESPACE IMAGE_NAME IMAGE_TAG"
  exit 1
fi

# Build the full Render deploy hook URL and specify the image to deploy
DEPLOY_URL="${RENDER_DEPLOY_HOOK}&imgURL=${IMAGE_REGISTRY}/${IMAGE_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}"

# Trigger the Render deploy hook and capture: response body & HTTP status code
RESPONSE=$(
  curl --silent --show-error \
    --request GET \
    --write-out "\nHTTP_STATUS:%{http_code}\n" \
    "$DEPLOY_URL" \
    2>&1
)

# Get http status from the response 
HTTP_STATUS=$(echo "$RESPONSE" | sed -n 's/HTTP_STATUS://p')

# Treat any non-2xx response as a deployment failure
if [ "$HTTP_STATUS" -lt 200 ] || [ "$HTTP_STATUS" -ge 300 ]; then
  echo "Render deploy hook failed"
  echo "$RESPONSE"
  exit 1
fi

# Deployment succeeded, print response
echo "Render deploy hook succeeded"
echo "$RESPONSE"
