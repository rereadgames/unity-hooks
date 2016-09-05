#!/bin/bash

if ! [ -d ".git" ]; then
    echo "Not in a git repository" >&2
    exit 1
fi

SCRIPT_DIR=$(cd "${0%/*}" && pwd)

ln -s $SCRIPT_DIR/hooks .git/hooks

echo "Installed Unity hooks."
