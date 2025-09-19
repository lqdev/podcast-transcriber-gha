import os
import sys
import requests
import tempfile
from pathlib import Path
from transformers import pipeline
import torch


class PodcastTranscriber:
    def __init__(self):
        """Initialize the transcriber with whisper-small model."""
        # Check if CUDA is available, otherwise use CPU
        device = 0 if torch.cuda.is_available() else "cpu"
        
        print(f"Using device: {device}")
        
        # Initialize the whisper pipeline
        self.transcriber = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny",
            device=device,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
    
    def download_audio(self, url: str, output_path: str) -> bool:
        """Download audio file from URL."""
        try:
            print(f"Downloading audio from: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Audio downloaded to: {output_path}")
            return True
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio file using whisper-small model."""
        try:
            print(f"Starting transcription of: {audio_path}")
            
            # Use the pipeline with long-form transcription settings
            result = self.transcriber(
                audio_path,
                chunk_length_s=30,  # Process in 30-second chunks
                stride_length_s=5,  # 5-second overlap between chunks
                return_timestamps=True
            )
            
            return result["text"]
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""
    
    def transcribe_from_url(self, url: str, output_file: str = None) -> str:
        """Download and transcribe audio from URL."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download audio to temporary file
            audio_path = os.path.join(temp_dir, "podcast_audio.mp3")
            
            if not self.download_audio(url, audio_path):
                return ""
            
            # Transcribe the audio
            transcript = self.transcribe_audio(audio_path)
            
            # Save transcript if output file specified
            if output_file and transcript:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(transcript)
                print(f"Transcript saved to: {output_file}")
            
            return transcript


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_url> [output_file]")
        print("Example: python main.py https://example.com/podcast.mp3 transcript.txt")
        return
    
    audio_url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Initialize transcriber
    transcriber = PodcastTranscriber()
    
    # Transcribe audio
    transcript = transcriber.transcribe_from_url(audio_url, output_file)
    
    if transcript:
        print("\n--- TRANSCRIPT ---")
        print(transcript)
        print("--- END TRANSCRIPT ---")
    else:
        print("Failed to transcribe audio.")


if __name__ == "__main__":
    main()
