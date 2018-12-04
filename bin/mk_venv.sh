#!/bin/bash

virtual_envs_path="$HOME/venvs"

if [ ! -d $virtual_env_paths ]; then
    mkdir -p $virtual_envs_path
fi

cd $virtual_envs_path

virtualenv -p /usr/bin/python3.6 AzuraBot

source AzuraBot/bin/activate
pip install --upgrade pip

