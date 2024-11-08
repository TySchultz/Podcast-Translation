import os
import sys
import argparse
from convertToSegments import convert_to_segments
from convertToSpanish import main as translate_to_spanish
from convertSegmentsToAudio import create_audio_from_segments
import os.path

def check_environment_variables():
    """Check if required API keys are set"""
    required_vars = ['REPLICATE_API_TOKEN', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        sys.exit(1)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Translate podcast from English to Spanish')
    parser.add_argument('input_file', help='Input audio file path (required)')
    parser.add_argument('--model', '-m', default='gpt-4o-mini', 
                      choices=['gpt-4o-mini', 'gpt-4o'],
                      help='OpenAI model to use for translation')
    parser.add_argument('--speaker0', 
                      default='alloy',
                      choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'],
                      help='Voice for SPEAKER_00')
    parser.add_argument('--speaker1', 
                      default='nova',
                      choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'],
                      help='Voice for SPEAKER_01')
    parser.add_argument('--workers', '-w',
                      type=int,
                      default=3,
                      help='Number of concurrent workers')
    return parser.parse_args()

def get_output_filename(input_file):
    """Generate output filename by adding _spanish before the extension"""
    base, ext = os.path.splitext(input_file)
    return f"{base}_spanish{ext}"

def main():
    print("🎙️ Starting Podcast Translation Process...")
    
    # Parse command line arguments
    args = parse_arguments()
    input_file = args.input_file
    model = args.model
    
    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Check environment variables
    check_environment_variables()
    
    try:
        # Step 1: Convert podcast to segments
        print(f"\n📝 Step 1: Converting podcast to segments...")
        convert_to_segments(input_file)
        print("✓ Successfully created segments")
        
        # Step 2: Translate segments to Spanish
        print("\n🔄 Step 2: Translating segments to Spanish...")
        translate_to_spanish(model=model)
        print("✓ Successfully translated segments")
        
        # Step 3: Convert translated text to audio
        output_file = get_output_filename(input_file)
        print("\n🔊 Step 3: Converting translated text to audio...")
        # Create voice mapping from arguments
        voice_mapping = {
            "SPEAKER_00": args.speaker0,
            "SPEAKER_01": args.speaker1
        }
        create_audio_from_segments(
            "translated_segments.json",
            final_output=output_file,
            max_workers=args.workers,
            speaker_voices=voice_mapping
        )
        print("✓ Successfully created Spanish audio")
        
        print("\n✨ Process completed successfully!")
        print(f"Final audio file: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
