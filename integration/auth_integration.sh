#!/bin/bash -e

. ./integration/utils.sh

data() {
    printf "{\"headers\": {\"Authorization\": \"%s\"}}" "${1}"
}

check_status() {
    echo "${1}"
    test $(echo "${1}" | jq ".statusCode") = "200"
}

basic-local() {
    echo "Invoking local basic-auth with expected status ${2}..."
    RESPONSE=$(sls invoke local -f basic-auth -d "$(data "${1}")")
    test $(echo "${RESPONSE}" | jq ".statusCode") = "${2}"
}

basic-remote() {
    echo "Invoking remote basic-auth with expected status ${2}..."
    RESPONSE=$(sls invoke -f basic-auth -d "$(data "${1}")")
    test $(echo "${RESPONSE}" | jq ".statusCode") = "${2}"
}

admin-local() {
    echo "Invoking local admin-auth with expected status ${2}..."
    RESPONSE=$(sls invoke local -f admin-auth -d "$(data "${1}")")
    test $(echo "${RESPONSE}" | jq ".statusCode") = "${2}"
}

admin-remote() {
    echo "Invoking remote admin-auth with expected status ${2}..."
    RESPONSE=$(sls invoke -f admin-auth -d "$(data "${1}")")
    test $(echo "${RESPONSE}" | jq ".statusCode") = "${2}"
}
