#!/bin/bash

virtual_env_path="$HOME/venvs/AzuraBot"

if [ -z "$VIRTUAL_ENV" ]; then
    
    if [ ! -d $virtual_env_path ]; then
        echo "Creating virtual env $virtual_env_path..."
        bin/mk_venv.sh
    fi

    echo "Activating virtual env $virtual_env_path..."
    . $virtual_env_path/bin/activate
fi

python azurabot.py
