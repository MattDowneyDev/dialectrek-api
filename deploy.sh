#!/usr/bin/env bash
# Builds the API's Docker image, pushes it to ECR, and rolls it out to Lambda.
# First run also provisions the ECR repo, IAM role, Lambda function, and HTTP API.
set -euo pipefail

REGION="us-east-1"
REPO_NAME="dialectrek-api"
FUNCTION_NAME="dialectrek-api"
ROLE_NAME="dialectrek-api-lambda-role"
API_NAME="dialectrek-api"
ARCHITECTURE="arm64"

cd "$(dirname "${BASH_SOURCE[0]}")"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"

echo "==> Ensuring ECR repo exists"
aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" >/dev/null 2>&1 || \
  aws ecr create-repository --repository-name "$REPO_NAME" --region "$REGION" >/dev/null

echo "==> Building image (linux/${ARCHITECTURE})"
docker build --platform "linux/${ARCHITECTURE}" -t "$REPO_NAME" .

echo "==> Logging in to ECR"
aws ecr get-login-password --region "$REGION" | \
  docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

IMAGE_TAG=$(date +%Y%m%d%H%M%S)
docker tag "${REPO_NAME}:latest" "${ECR_URI}:${IMAGE_TAG}"
docker tag "${REPO_NAME}:latest" "${ECR_URI}:latest"

echo "==> Pushing image"
docker push "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:latest"

if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" >/dev/null 2>&1; then
  echo "==> Updating existing Lambda function code"
  aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --image-uri "${ECR_URI}:${IMAGE_TAG}" \
    --region "$REGION" >/dev/null
  aws lambda wait function-updated --function-name "$FUNCTION_NAME" --region "$REGION"
else
  echo "==> First deploy: creating IAM role"
  if ! aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
    aws iam create-role \
      --role-name "$ROLE_NAME" \
      --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
          "Effect": "Allow",
          "Principal": {"Service": "lambda.amazonaws.com"},
          "Action": "sts:AssumeRole"
        }]
      }' >/dev/null
    aws iam attach-role-policy \
      --role-name "$ROLE_NAME" \
      --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    echo "==> Waiting for IAM role to propagate"
    sleep 10
  fi
  ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)

  echo "==> Creating Lambda function"
  for i in 1 2 3 4 5; do
    if aws lambda create-function \
      --function-name "$FUNCTION_NAME" \
      --package-type Image \
      --code ImageUri="${ECR_URI}:${IMAGE_TAG}" \
      --role "$ROLE_ARN" \
      --architectures "$ARCHITECTURE" \
      --timeout 10 \
      --memory-size 512 \
      --region "$REGION" >/dev/null 2>&1; then
      break
    fi
    echo "    role not ready yet, retrying in 5s..."
    sleep 5
  done
  aws lambda wait function-active --function-name "$FUNCTION_NAME" --region "$REGION"

  echo "==> Creating HTTP API (API Gateway)"
  FUNCTION_ARN=$(aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" --query 'Configuration.FunctionArn' --output text)
  aws apigatewayv2 create-api \
    --name "$API_NAME" \
    --protocol-type HTTP \
    --target "$FUNCTION_ARN" \
    --region "$REGION" >/dev/null
fi

API_ID=$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?Name=='${API_NAME}'].ApiId" --output text)
API_URL=$(aws apigatewayv2 get-api --api-id "$API_ID" --region "$REGION" --query 'ApiEndpoint' --output text)

echo ""
echo "Deployed. API base URL: ${API_URL}"
