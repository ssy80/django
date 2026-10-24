#!/bin/sh

# -I : Fetch the headers only
# -s : Silent mode (don't show progress meter or error messages)
# -i : Ignore case when matching headers
# '^location' : Match the 'Location' header (case-insensitive)

curl -s -I "$1" | grep -i '^location' | cut -d ' ' -f 2
