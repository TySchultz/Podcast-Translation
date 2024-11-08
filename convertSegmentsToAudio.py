import json
import os
import concurrent.futures
from openai import OpenAI
import soundfile as sf
import numpy as np

# Initialize OpenAI client
client = OpenAI()

def process_segment(segment, i, output_dir, total_segments, speaker_voices):
    """
    Process a single segment and return the audio file path and segment index
    """
    text = segment['text']
    speaker = segment['speaker']
    output_path = f"{output_dir}/segment_{i}.wav"
    
    try:
        # Show progress with segment details
        print(f"\nProcessing segment {i + 1}/{total_segments}")
        print(f"Speaker: {speaker}")
        print(f"Text: {text[:100]}..." if len(text) > 100 else f"Text: {text}")
        
        # Select voice based on speaker
        voice = speaker_voices[speaker]
        
        # Generate speech using OpenAI API
        print(f"Converting to speech using {voice} voice...")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Save the audio file
        print(f"Saving audio segment to {output_path}")
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Successfully processed segment {i + 1}/{total_segments}")
        return (output_path, i)  # Return tuple of path and index
        
    except Exception as e:
        print(f"❌ Error processing segment {i + 1}: {str(e)}")
        return None

def combine_audio_files(audio_files, output_file):
    """Combine multiple audio files into one"""
    # Read the first file to get sample rate
    data, sample_rate = sf.read(audio_files[0])
    combined = data
    
    # Append the rest of the files
    for file in audio_files[1:]:
        data, _ = sf.read(file)
        combined = np.concatenate((combined, data))
    
    # Write the combined audio
    sf.write(output_file, combined, sample_rate)

def create_audio_from_segments(json_file, output_dir="temp_audio", final_output="final_audio.wav", max_workers=3, speaker_voices=None):
    """
    Convert text segments to audio files and combine them into a single audio file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created temporary directory: {output_dir}")

    # Read JSON file
    print(f"Reading JSON file: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_segments = len(data['translated_segments'])
    print(f"Found {total_segments} segments to process")

    # Prepare arguments for parallel processing
    processed_segments = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_segment, 
                segment, 
                i, 
                output_dir, 
                total_segments,
                speaker_voices
            ) 
            for i, segment in enumerate(data['translated_segments'])
        ]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                processed_segments.append(result)

    # Sort segments by their original index
    processed_segments.sort(key=lambda x: x[1])
    
    # Combine audio files in correct order
    print("\nCombining audio segments...")
    audio_files = [path for path, _ in processed_segments]
    combine_audio_files(audio_files, final_output)
    
    # Clean up temporary files
    print("\nCleaning up temporary files...")
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    os.rmdir(output_dir)
    
    print(f"\n✓ Audio conversion complete! Final file saved as: {final_output}")
    print(f"Total segments processed: {len(processed_segments)}/{total_segments}")