import os
import json
import argparse
from mutagen import File  # Import the File class from mutagen


def get_audio_duration(filepath):
    """
    Get the duration of an audio file using mutagen.
    
    Args:
        filepath (str): Path to the audio file.
    
    Returns:
        float: Duration of the audio in seconds.
    """
    audio = File(filepath)  # Read the audio file with mutagen
    return audio.info.length  # Return the duration in seconds


def generate_manifest(audio_folder, transcription_folder, output_manifest_path):
    """
    Generate a training manifest JSONL file.
    
    Args:
        audio_folder (str): Path to the folder containing audio files.
        transcription_folder (str): Path to the folder containing transcription files.
        output_manifest_path (str): Path to save the output manifest JSONL file.
    """
    with open(output_manifest_path, 'w', encoding='utf-8') as manifest_file:
        # Get the list of audio files
        audio_files = [f for f in os.listdir(audio_folder) if f.startswith('audio_') and f.endswith(('.wav', '.mp3'))]
        
        for audio_file in audio_files:
            # Derive the corresponding transcription file name
            index = audio_file.split('_')[1].split('.')[0]  # Extract index from audio file (e.g., 'audio_0' -> '0')
            transcription_file = f"document_{index}.txt"
            
            # Build full paths for audio and transcription
            audio_path = os.path.join(audio_folder, audio_file)
            transcription_path = os.path.join(transcription_folder, transcription_file)
            
            # Check if corresponding transcription exists
            if os.path.exists(transcription_path):
                try:
                    # Get audio duration
                    duration = get_audio_duration(audio_path)
                    
                    # Read transcription
                    with open(transcription_path, 'r', encoding='utf-8') as transcription_file:
                        transcription_text = transcription_file.read().strip()
                    
                    # Create JSON line
                    manifest_entry = {
                        "audio_filepath": audio_path,
                        "duration": duration,
                        "text": transcription_text
                    }
                    manifest_file.write(json.dumps(manifest_entry) + '\n')
                
                except Exception as e:
                    print(f"Error processing {audio_file}: {e}")
            else:
                print(f"Warning: No transcription found for {audio_file}")
    
    print(f"Training manifest file saved to {output_manifest_path}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate a training manifest JSONL file.")
    parser.add_argument("-aud", "--audio_folder", required=True, help="Path to the folder containing audio files.")
    parser.add_argument("-tran", "--transcription_folder", required=True, help="Path to the folder containing transcription files.")
    parser.add_argument("-op", "--output_manifest", required=True, help="Path to save the output manifest JSONL file.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with the provided arguments
    generate_manifest(args.audio_folder, args.transcription_folder, args.output_manifest)
