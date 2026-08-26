#!/usr/bin/env bash
# Builds the API's Docker image and pushes it to ECR.
set -euo pipefail

# Use a dedicated AWS CLI profile scoped to just this app (see deploy-iam-policy.json).
export AWS_PROFILE="dialectrek-api"

REGION="us-east-1"
REPO_NAME="dialectrek-api"
DOCKER_PLATFORM="linux/amd64"

cd "$(dirname "${BASH_SOURCE[0]}")"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"

# Build the image. --provenance/--sbom disabled so Lambda can read the manifest.
echo "==> Building image (${DOCKER_PLATFORM})"
docker build --platform "$DOCKER_PLATFORM" --provenance=false --sbom=false -t "$REPO_NAME" .

# Log in to ECR.
echo "==> Logging in to ECR"
aws ecr get-login-password --region "$REGION" | \
  docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

# Tag with a timestamp and latest.
IMAGE_TAG=$(date +%Y%m%d%H%M%S)
docker tag "${REPO_NAME}:latest" "${ECR_URI}:${IMAGE_TAG}"
docker tag "${REPO_NAME}:latest" "${ECR_URI}:latest"

# Push both tags to ECR.
echo "==> Pushing image"
docker push "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:latest"

# Print how to roll the new image out to Lambda.
echo ""
echo "Pushed ${ECR_URI}:${IMAGE_TAG}"
echo "Point Lambda at it in the Console, or (using a profile with Lambda update permissions, not this one) run:"
echo "  aws lambda update-function-code --function-name dialecTrekApi --image-uri ${ECR_URI}:${IMAGE_TAG} --region ${REGION} --profile <your-admin-profile>"
