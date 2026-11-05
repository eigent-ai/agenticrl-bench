"""Test configuration and shared fixtures."""

import sys
import os

sys.path.insert(0, '/project/tests')

import Test_Login


def get_test_module():
    """Return the login test module for use in fixtures."""
    return Test_Login


def get_login_tests():
    """Retrieve available login test functions."""
    return [
        Test_Login.test_user_login,
        Test_Login.test_credentials,
    ]
