import json
import os
import concurrent.futures
from openai import OpenAI
from pydub import AudioSegment

# Initialize OpenAI client
client = OpenAI()

def process_segment(args):
    """
    Process a single segment and return the audio file path and segment index
    """
    segment, i, output_dir, total_segments = args
    text = segment['text']
    speaker = segment['speaker']
    output_path = f"{output_dir}/segment_{i}.mp3"
    
    try:
        # Show progress with segment details
        print(f"\nProcessing segment {i + 1}/{total_segments}")
        print(f"Speaker: {speaker}")
        print(f"Text: {text[:100]}..." if len(text) > 100 else f"Text: {text}")
        
        # Select voice based on speaker
        voice = "alloy" if speaker == "SPEAKER_00" else "onyx"
        
        # Generate speech using OpenAI API
        print(f"Converting to speech using {voice} voice...")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Save the audio file
        print(f"Saving audio segment to {output_path}")
        response.stream_to_file(output_path)
        
        print(f"✓ Successfully processed segment {i + 1}/{total_segments}")
        return (output_path, i)  # Return tuple of path and index
        
    except Exception as e:
        print(f"❌ Error processing segment {i + 1}: {str(e)}")
        return None

def create_audio_from_segments(json_file, output_dir="temp_audio", final_output="final_audio.mp3", max_workers=3):
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
    process_args = [
        (segment, i, output_dir, total_segments) 
        for i, segment in enumerate(data['translated_segments'])
    ]

    # Process segments in parallel
    processed_segments = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_segment, args) for args in process_args]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                processed_segments.append(result)

    # Sort segments by their original index
    processed_segments.sort(key=lambda x: x[1])
    
    # Combine audio files in correct order
    print("\nCombining audio segments...")
    combined_audio = AudioSegment.empty()
    for audio_path, _ in processed_segments:
        audio_segment = AudioSegment.from_mp3(audio_path)
        combined_audio += audio_segment
    
    # Export the final combined audio
    print(f"\nExporting final combined audio to {final_output}")
    combined_audio.export(final_output, format="mp3")
    
    # Clean up temporary files
    print("\nCleaning up temporary files...")
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    os.rmdir(output_dir)
    
    print(f"\n✓ Audio conversion complete! Final file saved as: {final_output}")
    print(f"Total segments processed: {len(processed_segments)}/{total_segments}")

if __name__ == "__main__":
    # Make sure you have set your OpenAI API key in environment variables
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Please set your OPENAI_API_KEY environment variable")
    
    create_audio_from_segments(
        "translated_segments.json",
        final_output="unispan_podcast_spanish.mp3",
        max_workers=3  # Adjust this number based on your needs
    )
