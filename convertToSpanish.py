import json
import os
from openai import OpenAI
from typing import List, Dict

def load_segments(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['output']['segments']

def translate_to_spanish(text: str, client: OpenAI, model: str, target_language: str) -> str:
    print(f"\nTranslating: {text}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
            {"role": "user", "content": text}
        ]
    )
    translated = response.choices[0].message.content
    print(f"Translated to: {translated}")
    return translated

def main(model: str = 'gpt-4o-mini', target_language: str = 'Spanish'):
    print("Starting translation process...")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Load segments from JSON
    print("\nLoading segments from JSON file...")
    segments = load_segments('convertedSegments.json')
    print(f"Loaded {len(segments)} segments to translate")
    
    # Translate each segment
    print(f"\nStarting translation of segments to {target_language}...")
    for i, segment in enumerate(segments, 1):
        print(f"\nTranslating segment {i}/{len(segments)}")
        original_text = segment['text']
        translated_text = translate_to_spanish(original_text, client, model, target_language)
        segment['text'] = translated_text
    
    # Save the translated segments
    print("\nSaving translated segments to file...")
    output_data = {
        "translated_segments": segments
    }
    
    with open('translated_segments.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print("\nTranslation complete! Results saved to 'translated_segments.json'")

if __name__ == "__main__":
    main()
