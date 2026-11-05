# Helper utility functions for CGI scripts
# This is a library file, sourced by other scripts

log_cgi() {
    echo "<!-- [HELPER] $1 -->"
}

check_cgi_status() {
    if [ $1 -eq 0 ]; then
        log_cgi "Status: OK"
    else
        log_cgi "Status: FAILED"
    fi
}
