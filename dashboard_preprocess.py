import os
import json
import pandas as pd
import re
import argparse
from collections import Counter


def process_jsonl(input_path, output_folder):
    """
    Process a JSONL file to extract audio metadata, compute statistics, 
    and save detailed and summary outputs to CSV files.

    Args:
        input_path (str): Path to the input JSONL file.
        output_folder (str): Path to the output folder.
    """
    # Validate output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Initialize lists to store extracted data
    audio_filepaths = []
    audio_ids = []
    durations = []
    texts = []
    
    # Reading the JSONL file
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            audio_filepaths.append(data["audio_filepath"])
            durations.append(data["duration"])
            texts.append(data["text"])
            # Extract audio ID from the file path
            audio_id = re.search(r'audio_(\d+)\.wav$', data["audio_filepath"])
            audio_ids.append(int(audio_id.group(1)) if audio_id else None)
    
    # Compute additional fields
    words_count = [len(text.split()) for text in texts]  # Number of words per utterance
    char_count = [len(text) for text in texts]           # Number of characters per utterance
    
    # Flatten all text to compute vocab and alphabet
    all_text = " ".join(texts).lower()
    vocabulary = set(re.findall(r'\b\w+\b', all_text))  # Unique words
    alphabet = set(all_text.replace(" ", ""))           # Unique characters
    
    # Compute duration bins with starting durations in minutes
    min_duration = min(durations)
    max_duration = max(durations)
    num_bins = 10
    
    # Generate bin edges and labels in minutes
    bin_edges = [min_duration + i * (max_duration - min_duration) / num_bins for i in range(num_bins + 1)]
    bin_labels = [f"{round(edge / 60, 1)} min" for edge in bin_edges[:-1]]
    
    # Assign durations to bins
    duration_bins = pd.cut(durations, bins=bin_edges, labels=bin_labels, include_lowest=True)
    
    # Prepare the final DataFrame
    data = {
        "audio_id": audio_ids,
        "audio_filepath": audio_filepaths,
        "duration": durations,
        "text": texts,
        "words_count": words_count,
        "char_count": char_count,
        "duration_bin": duration_bins,
    }
    
    df = pd.DataFrame(data)
    
    # Save summary statistics
    total_hours = sum(durations) / 3600
    total_utterances = len(audio_filepaths)
    vocab_size = len(vocabulary)
    alphabet_size = len(alphabet)
    
    summary = {
        "Total Hours": total_hours,
        "Total Utterances": total_utterances,
        "Vocabulary Size": vocab_size,
        "Alphabet Size": alphabet_size,
    }
    
    # Define output file paths
    detailed_output_path = os.path.join(output_folder, "detailed_data.csv")
    summary_output_path = os.path.join(output_folder, "summary_stats.csv")
    
    # Save detailed data to CSV
    df.to_csv(detailed_output_path, index=False)
    
    # Save summary stats
    pd.DataFrame([summary]).to_csv(summary_output_path, index=False)
    
    # Print summary
    print("Summary Statistics:")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print(f"Processed data with audio IDs and duration bins saved to {detailed_output_path}")
    print(f"Summary statistics saved to {summary_output_path}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process a JSONL file and save extracted data and statistics to CSV files.")
    parser.add_argument("-i", "--input_path", required=True, help="Path to the input JSONL file.")
    parser.add_argument("-o", "--output_folder", required=True, help="Path to the output folder where CSV files will be saved.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with the provided arguments
    process_jsonl(args.input_path, args.output_folder)
