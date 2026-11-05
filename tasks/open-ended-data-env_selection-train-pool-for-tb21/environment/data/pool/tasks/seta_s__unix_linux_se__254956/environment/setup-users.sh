#!/bin/sh
set -e

# Ensure mysql group with GID 999 exists (rename if the GID is already taken)
existing_grp=$(getent group 999 | cut -d: -f1 2>/dev/null || true)
if [ -n "$existing_grp" ] && [ "$existing_grp" != "mysql" ]; then
    groupmod -n mysql "$existing_grp"
elif [ -z "$existing_grp" ]; then
    groupadd -g 999 mysql
fi

# Ensure mysql user with UID 999 exists (rename if the UID is already taken)
existing_usr=$(id -un 999 2>/dev/null || true)
if [ -n "$existing_usr" ] && [ "$existing_usr" != "mysql" ]; then
    usermod -l mysql -d /nonexistent -s /bin/sh "$existing_usr"
elif [ -z "$existing_usr" ]; then
    useradd -r -u 999 -g 999 -d /nonexistent -s /bin/sh -M mysql
fi

# backupd group and user
getent group 3000 >/dev/null 2>&1 || groupadd -g 3000 backupd
id 3000 >/dev/null 2>&1 || useradd -m -u 3000 -g 3000 -s /bin/bash backupd

# dbadmin group and user
getent group 2000 >/dev/null 2>&1 || groupadd -g 2000 dbadmin
id 2000 >/dev/null 2>&1 || useradd -m -u 2000 -g 2000 -s /bin/bash dbadmin
