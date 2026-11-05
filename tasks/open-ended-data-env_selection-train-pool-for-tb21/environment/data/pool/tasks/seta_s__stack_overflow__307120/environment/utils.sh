#!/bin/bash
# Utility functions for environment setup

set_log_config() {
    declare -rx LOG_FORMAT='+%Y-%m-%d %H:%M:%S'
    declare -rx LOG_DIR='/var/log/webapp'
}
