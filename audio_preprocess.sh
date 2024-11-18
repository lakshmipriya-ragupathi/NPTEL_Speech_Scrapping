#!/bin/bash

# Function to display usage
usage() {
  echo "Usage: $0 <input_directory> <output_directory> <num_cpus>"
  exit 1
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
  usage
fi

# Get user inputs
INPUT_DIR=$1
OUTPUT_DIR=$2
NUM_CPUS=$3

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
  echo "ffmpeg is not installed. Please install it and try again."
  exit 1
fi

# Check if GNU parallel is installed
if ! command -v parallel &> /dev/null; then
  echo "GNU parallel is not installed. Please install it and try again."
  exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Find all mp3 files in the input directory
find "$INPUT_DIR" -type f -name '*.mp3' > mp3_files.txt

# Function to process a single file
process_file() {
  local input_file=$1
  local output_dir=$2
  local output_file="${output_dir}/$(basename "${input_file%.mp3}.wav")"

  ffmpeg -i "$input_file" -ar 16000 -ac 1 "$output_file" -y >/dev/null 2>&1
}

export -f process_file

# Process files in parallel using GNU parallel
cat mp3_files.txt | parallel -j "$NUM_CPUS" process_file {} "$OUTPUT_DIR"

# Clean up
rm mp3_files.txt

echo "Processing complete. Converted files are saved in $OUTPUT_DIR."
