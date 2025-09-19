import os
import re
import json
import sys
from pathlib import Path
from main import PodcastTranscriber


def process_github_issue():
    """Process GitHub issue and extract form data."""
    # Get issue data from GitHub context
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_title = os.environ.get('ISSUE_TITLE', '')
    
    print(f"Processing issue: {issue_title}")
    print(f"Issue body: {issue_body}")
    
    # Parse the issue body to extract form data
    # The issue body contains the form data in a specific format
    title = ""
    url = ""
    content = ""
    
    # Extract title, url, and content from the structured issue body
    lines = issue_body.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('### Title'):
            current_section = 'title'
            continue
        elif line.startswith('### Audio URL'):
            current_section = 'url'
            continue
        elif line.startswith('### Content'):
            current_section = 'content'
            continue
        elif line.startswith('###'):
            current_section = None
            continue
        
        if current_section == 'title' and line:
            title = line
        elif current_section == 'url' and line:
            url = line
        elif current_section == 'content' and line:
            if content:
                content += '\n' + line
            else:
                content = line
    
    if not title:
        title = issue_title.replace('[Transcription] ', '')
    
    return title, url, content


def create_transcript_file(title: str, content: str, transcript: str) -> str:
    """Create a markdown file with the transcript."""
    # Create transcripts directory if it doesn't exist
    transcripts_dir = Path("transcripts")
    transcripts_dir.mkdir(exist_ok=True)
    
    # Create filename from title
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '-', filename)
    filename = filename.strip('-').lower()
    
    if not filename:
        filename = "transcript"
    
    filepath = transcripts_dir / f"{filename}.md"
    
    # Create markdown content
    markdown_content = f"""# {title}

## User Commentary

{content}

## Transcript

{transcript}

---

*This transcript was automatically generated using OpenAI Whisper.*
"""
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return str(filepath)


def main():
    """Main function for GitHub Action processing."""
    try:
        # Extract issue data
        title, url, content = process_github_issue()
        
        if not title or not url:
            print("Error: Could not extract title or URL from issue")
            sys.exit(1)
        
        print(f"Extracted data:")
        print(f"  Title: {title}")
        print(f"  URL: {url}")
        print(f"  Content: {content[:100]}..." if content else "  Content: (empty)")
        
        # Validate the URL is an audio file
        audio_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac']
        url_lower = url.lower()
        
        if not any(ext in url_lower for ext in audio_extensions):
            print(f"Warning: URL may not be an audio file: {url}")
        
        # Initialize transcriber
        transcriber = PodcastTranscriber()
        
        # Transcribe audio
        print(f"Transcribing: {url}")
        transcript = transcriber.transcribe_from_url(url)
        
        if not transcript:
            print("Error: Failed to transcribe audio")
            sys.exit(1)
        
        # Create transcript file
        filepath = create_transcript_file(title, content, transcript)
        print(f"Transcript saved to: {filepath}")
        
        # Set output for GitHub Actions
        print(f"::set-output name=transcript_file::{filepath}")
        print(f"::set-output name=title::{title}")
        
    except Exception as e:
        print(f"Error processing issue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()