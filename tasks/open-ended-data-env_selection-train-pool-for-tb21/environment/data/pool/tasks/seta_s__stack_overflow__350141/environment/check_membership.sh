#!/bin/bash
# Check if a user is a member of a given group.
# Exit 0 if member, 1 if not.

if [ $# -ne 2 ]; then
    echo "Usage: $0 <username> <groupname>"
    exit 1
fi

USERNAME="$1"
GROUPNAME="$2"

id "$USERNAME" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "User '$USERNAME' does not exist." >&2
    exit 1
fi

GROUPS_OUTPUT=$(groups "$USERNAME" 2>/dev/null)

if echo "$GROUPS_OUTPUT" | grep -q "$GROUPNAME"; then
    exit 0
else
    exit 1
fi
