# Quick Start Guide - Podcast Transcriber

This guide will get you up and running with the Podcast Transcriber GitHub Action in just a few minutes.

## 🚀 Quick Setup

### Step 1: Copy the Project
1. Copy all files from this project to your GitHub repository
2. Ensure you have these key files:
   - `main.py` - Core transcription engine
   - `github_action_processor.py` - Issue processing logic
   - `postprocess_transcript.py` - AI cleanup script
   - `.github/ISSUE_TEMPLATE/podcast-transcription-request.yml` - Issue form
   - `.github/workflows/transcribe-podcast.yml` - GitHub Action workflow

### Step 2: Verify Setup
```bash
# Run the verification script
python verify_setup.py
```

### Step 3: Push to GitHub
```bash
git add .
git commit -m "Add podcast transcriber"
git push origin main
```

## 📝 How to Use

### Creating a Transcription Request

1. **Go to Issues**: Navigate to your repository's Issues tab
2. **New Issue**: Click "New issue" 
3. **Select Template**: Choose "Podcast Transcription Request"
4. **Fill the Form**:
   - **Title**: Enter a descriptive title
   - **Audio URL**: Provide the direct link to your audio file
   - **Content**: Add your commentary, show notes, or context (optional)

**Example:**
```
Title: Episode 301: The Future of AI
Audio URL: https://content.libsyn.com/podcast-episode.mp3
Content: This episode discusses the future of AI development and its impact on society.
Key guests include researchers from MIT and Stanford.
```

5. **Submit**: Click "Submit new issue"

### What Happens Next

The GitHub Action will automatically:

1. ✅ **Download** the audio file from your URL
2. ✅ **Transcribe** using OpenAI Whisper (whisper-small model)
3. ✅ **Clean up** the transcript with GitHub Models AI
4. ✅ **Create** a pull request with the final transcript
5. ✅ **Comment** on your issue with the results

## 📊 Expected Timeline

- **Small files** (< 10 minutes): ~2-5 minutes
- **Medium files** (10-30 minutes): ~5-15 minutes  
- **Large files** (30+ minutes): ~15-45 minutes

*Processing time depends on audio length and GitHub Actions queue*

## 🔧 Supported Audio Formats

- MP3, WAV, M4A, OGG, FLAC, AAC
- Most podcast hosting platforms (Libsyn, Anchor, etc.)
- Direct file URLs with authentication parameters

## 📁 Output Format

Your transcript will be saved as a markdown file in the `transcripts/` directory:

```markdown
# Episode Title

## User Commentary
[Your original content and commentary]

## Transcript
[Clean, formatted transcript with proper punctuation and paragraphs]

---
*This transcript was automatically generated using OpenAI Whisper and post-processed with GitHub Models for improved readability.*
```

## ❓ Troubleshooting

### Issue: Audio URL not found
- ✅ Ensure the URL is publicly accessible
- ✅ Check the URL points directly to an audio file
- ✅ Verify the URL includes proper file extension (.mp3, .wav, etc.)
- ✅ Test the URL in your browser to make sure it downloads

### Issue: Transcription failed
- ✅ Audio file might be corrupted
- ✅ Format might not be supported
- ✅ File might be too large (>100MB)
- ✅ Check if the URL requires authentication

### Issue: No pull request created
- ✅ Check GitHub Actions logs in the Actions tab
- ✅ Verify GitHub Models access is enabled
- ✅ Check repository permissions

## 💡 Pro Tips

1. **Audio Quality**: Higher quality audio = better transcripts
2. **File Size**: Smaller files process faster
3. **Clear Speech**: Podcasts with clear speakers work best
4. **Direct URLs**: Use direct links to audio files, not hosting page URLs
5. **URL Testing**: Test your audio URL in a browser before submitting
6. **Content Field**: Use the content field for context that helps with transcript accuracy

## 🆘 Getting Help

1. Check the Actions tab for detailed logs
2. Look at existing issues for similar problems
3. Create a new issue with:
   - Audio URL that failed
   - Error message from Actions log
   - Expected vs actual behavior
   - Whether the URL works when accessed directly

---

**Happy transcribing! 🎙️✨**