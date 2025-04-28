#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Error: Usage: $0 /path/to/input_dir /path/to/output_dir [--max_depth N]"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
MAX_DEPTH=""

if [ "$#" -eq 4 ] && [ "$3" = "--max_depth" ]; then
    if [[ "$4" =~ ^[0-9]+$ ]]; then
        MAX_DEPTH="--max_depth $4"
    else
        echo "Error: --max_depth requires a positive integer"
        exit 1
    fi
elif [ "$#" -gt 2 ]; then
    echo "Error: Invalid arguments. Usage: $0 /path/to/input_dir /path/to/output_dir [--max_depth N]"
    exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist"
    exit 1
fi

if [ ! -f "collect_files.py" ]; then
    echo "Error: collect_files.py not found in the current directory"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

python3 collect_files.py "$INPUT_DIR" "$OUTPUT_DIR" $MAX_DEPTH
if [ $? -ne 0 ]; then
    echo "Error: Failed to execute collect_files.py"
    exit 1
fi