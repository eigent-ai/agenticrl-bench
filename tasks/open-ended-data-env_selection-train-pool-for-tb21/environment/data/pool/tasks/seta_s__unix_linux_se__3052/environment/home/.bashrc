# ~/.bashrc: executed by bash for interactive non-login shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

APP_ENV=development
alias ll='ls -la'
alias mp='myproject-run'
