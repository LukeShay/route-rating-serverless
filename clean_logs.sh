#!/bin/bash

GROUPS=$(aws logs describe-log-groups | jq '.logGroups[].logGroupName')

echo "${GROUPS}"

IFS='" "' read -r -a LOG_GROUPS <<< "${GROUPS}"

for group in "${LOG_GROUPS[@]}"; do
    echo "${group//\"}"
    if [[ -n "${group//\"}" ]]; then
        aws logs delete-log-group --log-group-name "${group//\"}"
    fi
done
