#!/bin/bash

# Get the absolute path to the GPT4All-ui root directory
gpt4all_ui_root=$(cd "$(dirname "$0")/../../" && pwd)
gptq_backend_path=$(dirname "$0")

# Activate the GPT4All-ui virtual environment
source "$gpt4all_ui_root/env/bin/activate"

# Install the required packages
pip install -r "$gptq_backend_path/requirements.txt"

# Copy the gptq subfolder to the backends directory
cp -R "$gptq_backend_path/gptq" "$gpt4all_ui_root/backends/"

echo ""
echo "GPTQ_backend has been installed successfully!"
echo ""

# Deactivate the virtual environment
deactivate
