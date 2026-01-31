#!/bin/bash

# Deploy to Render and fail the job when deploy hook is unsuccessful
IMAGE_REGISTRY="${1}"
IMAGE_NAMESPACE="${2}"
IMAGE_NAME="${3}"
IMAGE_TAG="${4}"

if [[ $# -eq 0 ]]; then
  echo "usage: deploy.sh IMAGE_REGISTRY IMAGE_NAMESPACE IMAGE_NAME IMAGE_TAG"
  exit 1
fi

DEPLOY_URL="${RENDER_DEPLOY_HOOK}&imgURL=${IMAGE_REGISTRY}/${IMAGE_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}"

RESPONSE=$(
  curl --silent --show-error \
    --request GET \
    --write-out "\nHTTP_STATUS:%{http_code}\n" \
    "$DEPLOY_URL" \
    2>&1
)

HTTP_STATUS=$(echo "$RESPONSE" | sed -n 's/HTTP_STATUS://p')

if [ "$HTTP_STATUS" -lt 200 ] || [ "$HTTP_STATUS" -ge 300 ]; then
  echo "Render deploy hook failed"
  echo "$RESPONSE"
  exit 1
fi

echo "Render deploy hook succeeded"
echo "$RESPONSE"
