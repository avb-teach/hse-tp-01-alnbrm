#!/usr/bin/env python3

import os
import shutil
import sys
import argparse
from pathlib import Path

def collect_files(input_dir, max_depth):
    """Recursively collect file paths from input_dir up to max_depth."""
    input_dir = Path(input_dir).resolve()
    if not input_dir.is_dir():
        print(f"Error: Input directory '{input_dir}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    def traverse(current_dir, depth):
        if max_depth >= 0 and depth > max_depth:
            return
        try:
            for entry in current_dir.iterdir():
                if entry.is_file():
                    yield entry
                elif entry.is_dir() and (max_depth < 0 or depth < max_depth):
                    yield from traverse(entry, depth + 1)
        except Exception as e:
            print(f"Error accessing {current_dir}: {e}", file=sys.stderr)

    return traverse(input_dir, 1)

def copy_files(input_dir, output_dir, max_depth):
    """Copy files from input_dir to output_dir, flattening hierarchy and handling duplicates."""
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        print(f"Error: Failed to create output directory '{output_dir}'", file=sys.stderr)
        sys.exit(1)

    file_counts = {}
    
    for file_path in collect_files(input_dir, max_depth):
        filename = file_path.name
        base_name, ext = os.path.splitext(filename) if '.' in filename else (filename, '')
        
        target_path = output_dir / filename
        if target_path.exists():
            file_counts[base_name] = file_counts.get(base_name, 0) + 1
            new_filename = f"{base_name}{file_counts[base_name]}{ext}"
            target_path = output_dir / new_filename
        else:
            file_counts[base_name] = file_counts.get(base_name, 0)
        
        try:
            shutil.copy2(file_path, target_path)
        except Exception as e:
            print(f"Error: Failed to copy '{file_path}' to '{target_path}': {e}", file=sys.stderr)
    
    print(f"Files copied successfully to '{output_dir}'")

def main():
    parser = argparse.ArgumentParser(
        description="Collect files from input directory and copy to output directory, flattening hierarchy."
    )
    parser.add_argument("input_dir", help="Path to input directory")
    parser.add_argument("output_dir", help="Path to output directory")
    parser.add_argument(
        "--max_depth",
        type=int,
        default=-1,
        help="Maximum depth for directory traversal (default: no limit)"
    )
    
    args = parser.parse_args()
    
    if args.max_depth < -1 or args.max_depth == 0:
        print("Error: --max_depth must be a positive integer or -1 for no limit", file=sys.stderr)
        sys.exit(1)
    copy_files(args.input_dir, args.output_dir, args.max_depth)

if __name__ == "__main__":
    main()