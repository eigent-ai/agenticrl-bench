#!/usr/bin/env bash
# Container startup: the mount state is pre-seeded by the Dockerfile via mounts.db
# No real mounts are needed; the compliance system uses the mount state database.
exec sleep infinity
