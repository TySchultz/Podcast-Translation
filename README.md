# Podcast English-Spanish Translator

A command-line tool that translates podcast audio from English to multiple languages, allowing bilingual learning and comparison. Originally created to help translate a NotebookLLM podcast to Spanish, but now supports multiple languages.

## Features

- Transcribes English podcast audio to text
- Translates to multiple languages (50+ supported)
- Maintains original audio timing and pacing
- Preserves audio quality during translation
- Supports multiple speakers with different voices
- Concurrent processing for faster audio generation

## Prerequisites

- Python 3.7 or higher
- Internet connection for API access
- OpenAI API key
- Replicate API token

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/podcast-translator.git
```

2. Install required dependencies:

```bash
# Core dependencies
pip install openai
pip install requests
pip install python-dotenv
pip install replicate
pip install soundfile
pip install numpy

# Optional but recommended
pip install tqdm  # For progress bars
```

3. Set up your API keys:

```bash
# For Linux/Mac
export OPENAI_API_KEY='your-openai-key-here'
export REPLICATE_API_TOKEN='your-replicate-token-here'

# For Windows (Command Prompt)
set OPENAI_API_KEY=your-openai-key-here
set REPLICATE_API_TOKEN=your-replicate-token-here
```

## Usage

1. Place your English podcast audio file in the folder
2. Run the translation script using one of these commands:

```bash
# Basic usage
python TranslatePodcastToSpanish.py your_podcast.mp3

# Advanced usage with options
python TranslatePodcastToSpanish.py your_podcast.mp3 --language French --model gpt-4o --speaker0 fable --speaker1 shimmer --workers 4

# View all available options
python TranslatePodcastToSpanish.py --help
```

Available options:
- `--language, -l`: Target language for translation (default: Spanish)
- `--model, -m`: Translation model to use (gpt-4o-mini or gpt-4o)
- `--speaker0`: Voice for first speaker (alloy, echo, fable, onyx, nova, shimmer)
- `--speaker1`: Voice for second speaker (alloy, echo, fable, onyx, nova, shimmer)
- `--workers, -w`: Number of concurrent workers for audio processing (default: 3)

### Supported Languages
- Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

## Components

This project uses several key components:

- **Whisper Diarization** ([thomasmol/whisper-diarization](https://replicate.com/thomasmol/whisper-diarization)): Handles the initial audio transcription with speaker detection
  - Uses Whisper large-v3 model
  - Provides speaker diarization
  - Includes word & sentence level timestamps
  - Supports prompting and hotwords

- **OpenAI GPT-4o-mini**: Handles language translation
- **OpenAI TTS**: Converts translated text back to speech with multiple voice options

## Example Workflows

1. Translate podcast to French:
```bash
python TranslatePodcastToSpanish.py podcast.mp3 --language French
```

2. Use different voices for speakers:
```bash
python TranslatePodcastToSpanish.py podcast.mp3 --language German --speaker0 echo --speaker1 alloy
```

3. Optimize processing speed:
```bash
python TranslatePodcastToSpanish.py podcast.mp3 --language Spanish --workers 6
```

## Output

The script will generate a new audio file with the following naming convention:
`original_filename_targetlanguage.extension`


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
