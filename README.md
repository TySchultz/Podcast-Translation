# Podcast English-Spanish Translator

I created this to help translate a Notebookllm podcast to spanish. Its a rough implementation and wont get all of the inflection/nuances of NotebookLLM. 

A simple script that translates podcast audio from English to Spanish, allowing bilingual learning and comparison.

## Features

- Translates English podcast audio to Spanish
- Maintains original audio timing and pacing
- Preserves audio quality during translation

## Prerequisites

- Python 3.7 or higher
- Internet connection for API access

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
python TranslatePodcastToSpanish.py your_podcast.mp3 --model gpt-4o --speaker0 fable --speaker1 shimmer --workers 4

# View all available options
python TranslatePodcastToSpanish.py --help
```

Available options:
- `--model, -m`: Translation model to use (gpt-4o-mini or gpt-4o)
- `--speaker0`: Voice for first speaker (alloy, echo, fable, onyx, nova, shimmer)
- `--speaker1`: Voice for second speaker (alloy, echo, fable, onyx, nova, shimmer)
- `--workers, -w`: Number of concurrent workers for audio processing (default: 3)


## Components

This project uses several key components:

- **Whisper Diarization** ([thomasmol/whisper-diarization](https://replicate.com/thomasmol/whisper-diarization)): Handles the initial audio transcription with speaker detection
  - Uses Whisper large-v3 model
  - Provides speaker diarization
  - Includes word & sentence level timestamps
  - Supports prompting and hotwords

- **OpenAI GPT-4o-mini**: Handles Spanish translation
- **OpenAI TTS**: Converts translated text back to speech

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/podcast-translator/issues) page
2. Create a new issue if needed
3. Join our [Discord community](your-discord-link)
