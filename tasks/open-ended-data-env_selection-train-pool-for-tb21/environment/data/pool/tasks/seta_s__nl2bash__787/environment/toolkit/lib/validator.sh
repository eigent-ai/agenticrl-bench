# Config validator for ConfigCtl
# This file is sourced by common.sh

# Validate a config value against a rule
validate_value() {
    local key="$1"
    local value="$2"
    local rule="$3"

    case "$rule" in
        integer)
            [[ "$value" =~ ^[0-9]+$ ]] && return 0
            log_warn "Validation failed: $key='$value' is not an integer"
            return 1
            ;;
        boolean)
            [[ "$value" =~ ^(true|false|yes|no|on|off|0|1)$ ]] && return 0
            log_warn "Validation failed: $key='$value' is not a boolean"
            return 1
            ;;
        path)
            [[ "$value" =~ ^/ ]] && return 0
            log_warn "Validation failed: $key='$value' is not an absolute path"
            return 1
            ;;
        *)
            return 0  # No rule = always valid
            ;;
    esac
}

# Validate all keys in a parsed config against rules
validate_config() {
    local config_file="$1"
    local rules_output
    rules_output="$(load_rules)" || return 1

    local errors=0
    while IFS='=' read -r key value; do
        local rule
        rule=$(echo "$rules_output" | grep "^${key}=" | cut -d= -f2) || true
        if [[ -n "$rule" ]]; then
            validate_value "$key" "$value" "$rule" || ((errors++))
        fi
    done < <(parse_config "$config_file")

    return $errors
}
