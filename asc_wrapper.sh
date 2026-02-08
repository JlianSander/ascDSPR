#!/bin/bash
# Wrapper script for ascDSPR and a fallback complete solver

# Path to the shortcut solvers
SHORTCUTS=(
    "/home/lars/ascDSPR/build/asc_5/ascDSPR_ASC5"
    "/home/lars/ascDSPR/build/asc_6/ascDSPR_ASC6"
    "/home/lars/ascDSPR/build/asc_10/ascDSPR_ASC10"
)
# Path to the complete solver
FALLBACK="/home/lars/reducto/build/reducto"

check_result() {
    local output="$1"
    if echo "$output" | grep -q -w YES; then
        echo YES
        exit 0
    elif echo "$output" | grep -q -w NO; then
        echo NO
        exit 0
    elif echo "$output" | grep -q -w UNKNOWN; then
        return 1
    else
        echo "$output"
        exit 1
    fi
}

# Go through all shortcuts and return the result immediately, otherwise continue with the next shortcut
for shortcut in "${SHORTCUTS[@]}"; do
    OUTPUT=$("$shortcut" "$@")
    check_result "$OUTPUT"
done

# If no shortcut was successfull, use the complete solver
$FALLBACK "$@"
exit $?
