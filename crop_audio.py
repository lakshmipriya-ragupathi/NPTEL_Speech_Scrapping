import os
import wave
import contextlib
import argparse


def crop_last_10_seconds(input_folder, output_folder):
    """
    Crops the last 10 seconds from all .wav files in the input folder and saves the cropped files in the output folder.

    Args:
        input_folder (str): Path to the folder containing input .wav files.
        output_folder (str): Path to the folder where cropped .wav files will be saved.

    Outputs:
        Cropped .wav files are saved in the specified output folder.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each .wav file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            with contextlib.closing(wave.open(input_path, 'rb')) as wav_file:
                # Extract audio parameters
                params = wav_file.getparams()
                n_channels = params.nchannels
                sampwidth = params.sampwidth
                framerate = params.framerate
                n_frames = params.nframes
                
                # Calculate the total duration
                duration = n_frames / float(framerate)
                
                # Calculate the number of frames for the last 10 seconds
                crop_frames = max(0, int((duration - 10) * framerate))
                
                # Read the frames up to the cropped position
                wav_file.rewind()
                frames_to_save = wav_file.readframes(crop_frames)
                
                # Write the cropped frames to the new file
                with wave.open(output_path, 'wb') as cropped_wav:
                    cropped_wav.setnchannels(n_channels)
                    cropped_wav.setsampwidth(sampwidth)
                    cropped_wav.setframerate(framerate)
                    cropped_wav.writeframes(frames_to_save)
                    
            print(f"Cropped: {filename} -> {output_path}")

if __name__ == "__main__":
    """
    Parses command-line arguments and calls the crop_last_10_seconds function with the specified input and output paths.
    """
    parser = argparse.ArgumentParser(description="Crop the last 10 seconds from .wav files in the input folder and save them to the output folder.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input folder containing .wav files.")
    parser.add_argument('-o', '--output', required=True, help="Path to the output folder where cropped files will be saved.")
    
    args = parser.parse_args()
    
    # Call the crop function with the provided arguments
    crop_last_10_seconds(args.input, args.output)
