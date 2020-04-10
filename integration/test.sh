#!/bin/bash -e

. ./integration/utils.sh
. ./integration/auth_integration.sh

test-local() {
    echo "Testing basic auth..."
    basic-local "${TEST_VALID_ADMIN_JWT}" "200" || exit-message "Valid basic auth failed." "${?}"
    basic-local "${TEST_VALID_BASIC_JWT}" "200" || exit-message "Valid basic auth failed." "${?}"
    basic-local "${TEST_INVALID_JWT}" "403" || exit-message "Invalid basic auth failed." "${?}"

    echo "Testing admin auth..."
    admin-local "${TEST_VALID_ADMIN_JWT}" "200" || exit-message "Valid admin auth failed." "${?}"
    admin-local "${TEST_VALID_BASIC_JWT}" "401" || exit-message "Unauthorized admin auth failed." "${?}"
    admin-local "${TEST_INVALID_JWT}" "403" || exit-message "Invalid admin auth failed." "${?}"
}

eval "${@}"
