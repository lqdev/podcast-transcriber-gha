import os
import sys
import requests
import json
from pathlib import Path


def call_github_models(prompt: str, max_tokens: int = 4000) -> str:
    """Call GitHub Models API to post-process the transcript."""
    
    # GitHub Models API endpoint
    url = "https://models.github.ai/inference/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    # Use GPT-4 for better text processing
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": """You are a professional transcript editor. Your job is to clean up and improve automatically generated transcripts while maintaining accuracy and the speaker's original meaning.

Please:
1. Fix obvious transcription errors and improve readability
2. Add proper punctuation and capitalization
3. Break text into logical paragraphs
4. Remove filler words (um, uh, like) unless they add meaning
5. Maintain the conversational tone and speaker's voice
6. Don't add information that wasn't spoken
7. Format the output as clean, readable prose

Return only the cleaned transcript without any additional commentary."""
            },
            {
                "role": "user",
                "content": f"Please clean up this podcast transcript:\n\n{prompt}"
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except Exception as e:
        print(f"Error calling GitHub Models API: {e}")
        return None


def process_transcript_file(filepath: str) -> str:
    """Process the transcript file and return cleaned version."""
    
    # Read the original transcript file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the transcript section
    lines = content.split('\n')
    transcript_start = -1
    
    for i, line in enumerate(lines):
        if line.strip() == "## Transcript":
            transcript_start = i + 1
            break
    
    if transcript_start == -1:
        print("Error: Could not find transcript section")
        return None
    
    # Get the raw transcript
    transcript_lines = lines[transcript_start:]
    raw_transcript = '\n'.join(transcript_lines).strip()
    
    # Remove the footer if present
    if "---" in raw_transcript:
        raw_transcript = raw_transcript.split("---")[0].strip()
    
    print("Calling GitHub Models API to clean up transcript...")
    
    # Clean up the transcript using GitHub Models
    cleaned_transcript = call_github_models(raw_transcript)
    
    if not cleaned_transcript:
        print("Warning: Failed to clean transcript, using original")
        cleaned_transcript = raw_transcript
    
    # Reconstruct the file with cleaned transcript
    header_lines = lines[:transcript_start]
    header_content = '\n'.join(header_lines)
    
    cleaned_content = f"""{header_content}

{cleaned_transcript}

---

*This transcript was automatically generated using OpenAI Whisper and post-processed with GitHub Models for improved readability.*
"""
    
    # Write to new file
    original_path = Path(filepath)
    cleaned_path = original_path.parent / f"{original_path.stem}_cleaned{original_path.suffix}"
    
    with open(cleaned_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    return str(cleaned_path)


def main():
    """Main function for post-processing."""
    transcript_file = os.environ.get('TRANSCRIPT_FILE')
    
    if not transcript_file:
        print("Error: TRANSCRIPT_FILE environment variable not set")
        sys.exit(1)
    
    if not os.path.exists(transcript_file):
        print(f"Error: Transcript file not found: {transcript_file}")
        sys.exit(1)
    
    print(f"Post-processing transcript: {transcript_file}")
    
    # Process the transcript
    cleaned_file = process_transcript_file(transcript_file)
    
    if not cleaned_file:
        print("Error: Failed to process transcript")
        sys.exit(1)
    
    print(f"Cleaned transcript saved to: {cleaned_file}")
    
    # Set output for GitHub Actions
    print(f"::set-output name=cleaned_file::{cleaned_file}")


if __name__ == "__main__":
    main()