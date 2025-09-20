import os
import sys
import requests
import json
import shutil
from pathlib import Path


def call_github_models(prompt: str, max_tokens: int = 4000) -> str:
    """Call GitHub Models API to post-process the transcript."""
    
    # GitHub Models API endpoint - try multiple possible endpoints
    endpoints = [
        "https://models.inference.ai.azure.com/chat/completions",
        "https://api.githubcopilot.com/chat/completions",
        "https://models.github.ai/chat/completions"
    ]
    
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
    
    # Try each endpoint until one works
    for url in endpoints:
        try:
            print(f"Trying GitHub Models API endpoint: {url}")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            print("✅ GitHub Models API call successful")
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error with endpoint {url}: {e}")
            if e.response.status_code == 403:
                print("   This usually means the repository doesn't have access to GitHub Models")
            continue
        except Exception as e:
            print(f"❌ Error with endpoint {url}: {e}")
            continue
    
    print("⚠️  All GitHub Models API endpoints failed, will use original transcript")
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
        print("Error: Failed to process transcript, using original file")
        # Create a copy of the original with "_cleaned" suffix as fallback
        original_path = Path(transcript_file)
        cleaned_file = str(original_path.parent / f"{original_path.stem}_cleaned{original_path.suffix}")
        
        # Copy original to cleaned location
        import shutil
        shutil.copy2(transcript_file, cleaned_file)
        print(f"⚠️  Fallback: Copied original to {cleaned_file}")
    
    print(f"Cleaned transcript saved to: {cleaned_file}")
    
    # Set output for GitHub Actions using environment file
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"cleaned_file={cleaned_file}\n")
    else:
        # Fallback to deprecated method for backwards compatibility
        print(f"::set-output name=cleaned_file::{cleaned_file}")


if __name__ == "__main__":
    main()