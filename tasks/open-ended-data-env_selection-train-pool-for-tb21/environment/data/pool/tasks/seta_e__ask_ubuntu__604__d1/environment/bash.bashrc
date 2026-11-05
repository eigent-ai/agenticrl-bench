# System-wide .bashrc file for interactive bash shells.

# If not running interactively, do not do anything
[ -z "$PS1" ] && return

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (with debian_chroot if present)
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
