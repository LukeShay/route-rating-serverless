#!/bin/bash -e

. ./integration/utils.sh
. ./integration/auth_integration.sh

run-tests() {
    echo "Testing basic auth..."
    basic-"${1}" "${TEST_VALID_ADMIN_JWT}" "200" || exit-message "Valid basic auth failed." "${?}"
    basic-"${1}" "${TEST_VALID_BASIC_JWT}" "200" || exit-message "Valid basic auth failed." "${?}"
    basic-"${1}" "${TEST_INVALID_JWT}" "403" || exit-message "Invalid basic auth failed." "${?}"

    echo "Testing admin auth..."
    admin-"${1}" "${TEST_VALID_ADMIN_JWT}" "200" || exit-message "Valid admin auth failed." "${?}"
    admin-"${1}" "${TEST_VALID_BASIC_JWT}" "401" || exit-message "Unauthorized admin auth failed." "${?}"
    admin-"${1}" "${TEST_INVALID_JWT}" "403" || exit-message "Invalid admin auth failed." "${?}"
}


test-local() {
    run-tests "local"
}

test-remote() {
    run-tests "remote"
}

eval "${@}"
