import os
import sys
from convertToSegments import upload_to_replicate
from convertToSpanish import main as translate_to_spanish
from convertSegmentsToAudio import create_audio_from_segments

def check_environment_variables():
    """Check if required API keys are set"""
    required_vars = ['REPLICATE_API_TOKEN', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        sys.exit(1)

def main():
    print("🎙️ Starting Podcast Translation Process...")
    
    # Check environment variables
    check_environment_variables()
    
    try:
        # Step 1: Convert podcast to segments
        print("\n📝 Step 1: Converting podcast to segments...")
        upload_to_replicate("UnispanPodcast.wav")
        print("✓ Successfully created segments")
        
        # Step 2: Translate segments to Spanish
        print("\n🔄 Step 2: Translating segments to Spanish...")
        translate_to_spanish()
        print("✓ Successfully translated segments")
        
        # Step 3: Convert translated text to audio
        print("\n🔊 Step 3: Converting translated text to audio...")
        create_audio_from_segments(
            "translated_segments.json",
            final_output="unispan_podcast_spanish.mp3",
            max_workers=3
        )
        print("✓ Successfully created Spanish audio")
        
        print("\n✨ Process completed successfully!")
        print("Final audio file: unispan_podcast_spanish.mp3")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
