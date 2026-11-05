#!/sbin/openrc-run
# Stub acpid init script for container environment

name="acpid"
description="ACPI event daemon"

depend() {
    need localmount
}

start() {
    ebegin "Starting $name"
    eend 0
}

stop() {
    ebegin "Stopping $name"
    eend 0
}
