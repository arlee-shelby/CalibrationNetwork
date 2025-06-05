#!/bin/bash

set -e

env_name="NabEnv"
py_file_name="main.py"
run_folder="Runs7400"
run_numbers="7485 7486"
run_numbers_array=($run_numbers)

if conda env list | grep -q "*"; then
  echo "Conda environment is activated."
  if [ "$CONDA_DEFAULT_ENV" == "$env_name" ]; then
    echo "Conda enviorment activated: $CONDA_DEFAULT_ENV"
  fi
else
  echo "No conda environment activated."
  exit 1
fi

echo "Checking .py file exists"
if [ ! -f "$py_file_name" ]; then
   echo "Error: .py file does not exist"
   exit 1
else
    echo "It exists"
fi

for run in ${run_numbers_array[@]}; do
    echo "Running script for run: $run"
    python "$py_file_name" -rf "$run_folder" -r "$run"
done

echo "Sucessfully fit peaks for runs: $run_numbers_array"