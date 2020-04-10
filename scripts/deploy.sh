#!/bin/bash

generate_secrets() {
  echo "{'JWT_SECRET': '${JWT_SECRET}', 'REFRESH_SECRET': '${REFRESH_SECRET}'}" | sed "s/'/\"/g" | jq . > secrets.json
}

sls_deploy() {
  serverless deploy
}

main() {
  generate_secrets
  sls_deploy
}

main
