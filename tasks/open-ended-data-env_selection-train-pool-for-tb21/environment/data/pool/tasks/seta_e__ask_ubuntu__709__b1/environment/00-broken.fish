# System environment setup
if [ -d /usr/local/bin ]; then
    set -gx PATH /usr/local/bin $PATH
fi

# This was supposed to set a variable but uses bash syntax
export DEVTEAM_ENV="production"
