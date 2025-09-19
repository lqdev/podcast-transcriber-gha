# Podcast Transcriber GitHub Action

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

Bootstrap, build, and test the repository:
- Install uv package manager: `pip install uv`
- Sync dependencies: `uv sync` -- NEVER CANCEL: Takes 60-600 seconds on first run (downloads PyTorch, transformers, Whisper models). Set timeout to 900+ seconds.
- Verify setup: `uv run python verify_setup.py` -- Takes 120 seconds. NEVER CANCEL. Set timeout to 180+ seconds.
- Run tests: `uv run python test_processor.py` -- Takes 60 seconds. NEVER CANCEL. Set timeout to 120+ seconds.

## Validation

ALWAYS run through complete validation after making changes:
- Syntax validation: `uv run python verify_setup.py` validates Python and YAML syntax
- Test suite: `uv run python test_processor.py` validates issue processing, transcript creation, and URL validation
### Manual Validation Scenarios
**CRITICAL**: After making changes, always test these complete scenarios:

1. **Issue Processing Validation**:
   ```bash
   export ISSUE_TITLE="[Transcription] Test Episode"
   export ISSUE_BODY="### Title\nTest Episode\n### Audio URL\nhttps://example.com/test.mp3\n### Content\nTest content"
   uv run python github_action_processor.py
   # Verify: Transcript file created in transcripts/ directory
   ```

2. **Postprocessing Validation**:
   ```bash
   # Create test transcript file first
   export TRANSCRIPT_FILE="transcripts/test-file.md" 
   export GITHUB_TOKEN="your-token"  # Optional for testing
   uv run python postprocess_transcript.py
   # Verify: Cleaned transcript file created with "_cleaned" suffix
   ```

3. **End-to-End Workflow Test**: 
   - Create real GitHub issue using the template
   - Monitor GitHub Actions execution
   - Verify pull request creation with final transcript

**Note**: Transcription requires internet access to Hugging Face. In restricted environments, transcription will fail with model loading errors - this is expected behavior.
- Always run both verification scripts before committing changes

## Critical Timing Expectations

**NEVER CANCEL** these operations - they require extended time:
- `uv sync` (initial): 600-900 seconds (downloads ~2GB of ML models and dependencies)
- Model loading (first time): 300+ seconds (downloads OpenAI Whisper model from Hugging Face)
- Transcription: 60-600+ seconds (varies with audio length - 1-10x audio duration)
- GitHub Models API postprocessing: 30-120 seconds (depends on transcript length)
- Complete verification: 120-180 seconds (runs all syntax checks and tests)

**CRITICAL**: In environments without internet access to Hugging Face, transcription will fail with model loading errors. This is expected - the workflow requires internet connectivity for model downloads on first run.

## Project Structure

```
├── main.py                           # Core transcription engine (OpenAI Whisper)
├── github_action_processor.py        # GitHub issue processing and workflow orchestration
├── postprocess_transcript.py         # AI-powered transcript cleanup using GitHub Models
├── test_processor.py                 # Test suite for issue processing and validation
├── verify_setup.py                   # Pre-commit verification script
├── setup_check.py                    # Repository setup validation
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── podcast-transcription-request.yml  # GitHub issue form template
│   └── workflows/
│       └── transcribe-podcast.yml     # Main GitHub Action workflow
├── transcripts/                      # Generated transcripts (auto-created)
├── pyproject.toml                    # Python dependencies (uv managed)
└── uv.lock                          # Dependency lock file
```

## Common Tasks

Always validate commands work before documenting them:

### Build and Dependencies
```bash
# Install package manager
pip install uv

# Sync dependencies (FIRST TIME - NEVER CANCEL)
uv sync  # 600-900 seconds timeout required

# Check dependencies after initial sync
uv sync --check  # 60 seconds timeout
```

### Testing and Validation
```bash
# Run complete verification suite
uv run python verify_setup.py  # 180 seconds timeout

# Run test suite only
uv run python test_processor.py  # 120 seconds timeout

# Test specific components
uv run python setup_check.py  # Quick setup validation
```

### Local Development and Testing
```bash
# Test transcription locally (requires internet for model download)
uv run python main.py "https://example.com/audio.mp3" output.txt

# Test issue processing (set env vars)
export ISSUE_TITLE="Test Episode"
export ISSUE_BODY="### Title\nTest\n### Audio URL\nhttps://example.com/test.mp3\n### Content\nTest content"
uv run python github_action_processor.py

# Test postprocessing (requires GITHUB_TOKEN)
export TRANSCRIPT_FILE="transcripts/test-file.md" 
export GITHUB_TOKEN="your-token"
uv run python postprocess_transcript.py
```

## Workflow Components

### Issue Processing Flow
1. User creates GitHub issue using template (`.github/ISSUE_TEMPLATE/podcast-transcription-request.yml`)
2. GitHub Action triggers on issue creation with "transcription" label
3. `github_action_processor.py` extracts title, audio URL, content from issue body
4. `main.py` downloads audio and transcribes using OpenAI Whisper (whisper-small model)
5. `postprocess_transcript.py` cleans transcript using GitHub Models API
6. GitHub Action creates pull request with final transcript

### Supported Audio Formats
MP3, WAV, M4A, OGG, FLAC, AAC - validated by file extension in URL

### Expected Timeline for Complete Workflow
- Issue creation to workflow start: 10-30 seconds
- Dependency setup: 60-120 seconds (cached after first run)
- Audio download: 10-60 seconds (depends on file size)
- Transcription: 60-600+ seconds (depends on audio length)
- AI postprocessing: 30-120 seconds
- Pull request creation: 10-30 seconds
- **Total**: 3-15 minutes for typical podcast episode

## Environment Requirements

### Prerequisites
- Python 3.12+ (specified in `.python-version`)
- `uv` package manager
- Internet access for:
  - Hugging Face model downloads (Whisper)
  - GitHub Models API access
  - Audio file downloads

### GitHub Action Requirements
- **GitHub Token**: Automatically provided (`secrets.GITHUB_TOKEN`)
- **GitHub Models Access**: Repository must have access to GitHub Models
- **Permissions**: `contents: write`, `pull-requests: write`, `issues: write`

### Debugging and Troubleshooting

**Common Issues and Solutions**:
1. **Model loading fails**: `We couldn't connect to 'https://huggingface.co'`
   - **Cause**: Network connectivity to Hugging Face required for model downloads
   - **Solution**: Ensure internet access or use cached models
   - **Expected**: This will fail in sandboxed/restricted environments

2. **Postprocessing fails**: `Error calling GitHub Models API`
   - **Cause**: Missing GITHUB_TOKEN or no GitHub Models access
   - **Solution**: Check token permissions and repository access to GitHub Models
   - **Fallback**: System uses original transcript if API fails

3. **Audio download fails**: `Error downloading audio`
   - **Cause**: URL not accessible or not direct link to audio file
   - **Solution**: Verify URL is direct link to audio file, test in browser

4. **Workflow doesn't trigger**: GitHub Action not starting
   - **Cause**: Issue missing "transcription" label or wrong repository owner
   - **Solution**: Ensure issue has "transcription" label and is created by repo owner

**Validation Commands**:
```bash
# Repository setup validation
uv run python setup_check.py

# Complete verification with timing
uv run python verify_setup.py  # ~120 seconds

# Test suite validation  
uv run python test_processor.py  # ~60 seconds

# YAML syntax validation (included in verify_setup.py)
python -c "import yaml; yaml.safe_load(open('.github/workflows/transcribe-podcast.yml'))"
```

### Log Locations
- GitHub Actions logs: Repository Actions tab
- Local testing: Console output from `uv run` commands
- Transcript files: `transcripts/` directory

## Development Guidelines

### Making Changes
1. Always run `uv run python verify_setup.py` before and after changes
2. Update tests in `test_processor.py` for new functionality
3. Test locally with sample data before pushing
4. Validate GitHub Actions workflow syntax if modifying `.github/workflows/`

### Code Style
- Python 3.12+ syntax
- Type hints where appropriate
- Comprehensive error handling with descriptive messages
- Environment variable configuration for GitHub Actions integration

### Dependencies
- Use `uv add <package>` to add new dependencies
- Run `uv sync` after adding dependencies
- Commit both `pyproject.toml` and `uv.lock` changes

## File Content Examples

### Sample Issue Body Format
```
### Title
Episode 301: The Future of AI Development

### Audio URL
https://example.com/podcast-episode.mp3

### Content
This episode covers fascinating topics about AI development and includes 
interviews with leading researchers. Key topics include neural networks, 
machine learning applications, and future predictions.
```

### Sample Transcript Output
```markdown
# Episode 301: The Future of AI Development

## User Commentary
This episode covers fascinating topics about AI development...

## Transcript
[Transcribed content from Whisper]

---
*This transcript was automatically generated using OpenAI Whisper and post-processed with GitHub Models for improved readability.*
```