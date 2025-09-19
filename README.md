# Podcast Transcriber GitHub Action

An automated podcast transcription system using OpenAI Whisper and GitHub Actions. Submit a GitHub issue with an audio URL, and get back a cleaned, formatted transcript via pull request.

## Features

- 🎙️ **Automatic Transcription**: Uses OpenAI Whisper-small model for high-quality speech-to-text
- 🤖 **AI Post-Processing**: Leverages GitHub Models to clean and format transcripts
- 🔄 **Automated Workflow**: Complete automation from issue submission to PR creation
- 📝 **Professional Output**: Generates clean, readable markdown transcripts
- 🚀 **Zero Setup**: Just submit an issue and let GitHub Actions handle the rest

## How to Use

1. **Create an Issue**: Go to the Issues tab and click "New Issue"
2. **Select Template**: Choose "Podcast Transcription Request" 
3. **Fill the Form**:
   - **Title**: Enter a descriptive title for your podcast episode
   - **Audio URL**: Provide the direct link to your audio file
   - **Content**: Add any commentary, show notes, or context (optional)
   
   Example:
   ```
   Title: Episode 301: The Future of AI Development
   Audio URL: https://example.com/podcast-episode.mp3
   Content: This episode covers fascinating topics about AI development and includes 
   interviews with leading researchers. Key topics include neural networks, 
   machine learning applications, and future predictions.
   ```

4. **Submit**: The GitHub Action will automatically:
   - Download the audio file from the provided URL
   - Transcribe it using Whisper
   - Clean up the transcript with AI
   - Create a pull request with the final result

## Supported Audio Formats

- MP3
- WAV
- M4A
- OGG
- FLAC
- AAC

## Project Structure

```
├── main.py                           # Core transcription script
├── github_action_processor.py        # GitHub Action issue processing
├── postprocess_transcript.py         # AI-powered transcript cleanup
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── podcast-transcription-request.yml  # Issue form template
│   └── workflows/
│       └── transcribe-podcast.yml     # Main GitHub Action workflow
├── transcripts/                      # Generated transcripts (auto-created)
├── pyproject.toml                    # Python dependencies
└── README.md                         # This file
```

## Local Development

### Prerequisites

- [uv](https://github.com/astral-sh/uv) package manager
- Python 3.12+

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd podcast-transcriber-gha
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Test transcription locally:
   ```bash
   uv run python main.py "https://example.com/audio.mp3" output.txt
   ```

### GitHub Action Configuration

The workflow requires:
- **GitHub Token**: Automatically provided by GitHub Actions
- **GitHub Models Access**: Ensure your repository has access to GitHub Models

## Technical Details

### Transcription Process

1. **Audio Download**: Downloads audio from the provided URL
2. **Whisper Processing**: Uses OpenAI Whisper-small with chunked processing for long-form audio
3. **AI Cleanup**: Leverages GitHub Models (GPT-4) to:
   - Fix transcription errors
   - Add proper punctuation
   - Remove filler words
   - Format into readable paragraphs
4. **Output Generation**: Creates a markdown file with:
   - Original user commentary
   - Cleaned transcript
   - Metadata

### Performance

- **Model**: OpenAI Whisper-small (CPU optimized)
- **Processing**: Chunked processing for long audio files
- **Memory**: Efficient memory usage with temporary file handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

[Add your license here]

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with the bug report template
3. Provide audio URL and error details

---

**Made with ❤️ and powered by OpenAI Whisper + GitHub Models**
