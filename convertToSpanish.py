import json
import os
from openai import OpenAI
from typing import List, Dict

def load_segments(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['output']['segments']

def translate_to_spanish(text: str, client: OpenAI, model: str) -> str:
    print(f"\nTranslating: {text}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a translator. Translate the following text to Spanish."},
            {"role": "user", "content": text}
        ]
    )
    translated = response.choices[0].message.content
    print(f"Translated to: {translated}")
    return translated

def main(model: str = 'gpt-4o-mini'):
    print("Starting translation process...")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Load segments from JSON
    print("\nLoading segments from JSON file...")
    segments = load_segments('convertedSegments.json')
    print(f"Loaded {len(segments)} segments to translate")
    
    # Translate each segment
    print("\nStarting translation of segments...")
    for i, segment in enumerate(segments, 1):
        print(f"\nTranslating segment {i}/{len(segments)}")
        original_text = segment['text']
        spanish_text = translate_to_spanish(original_text, client, model)
        segment['text'] = spanish_text
    
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
