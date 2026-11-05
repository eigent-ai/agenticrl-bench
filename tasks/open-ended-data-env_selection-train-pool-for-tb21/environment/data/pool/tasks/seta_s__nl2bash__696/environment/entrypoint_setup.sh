#!/bin/bash
/setup_data.sh
exec "${@:-bash}"
