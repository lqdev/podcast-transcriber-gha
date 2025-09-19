#!/usr/bin/env python3
"""
Setup script for the Podcast Transcriber GitHub Action.
This script helps ensure the repository is properly configured.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath: Path, description: str) -> bool:
    """Check if a required file exists."""
    if filepath.exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} (missing: {filepath})")
        return False


def check_directory_exists(dirpath: Path, description: str) -> bool:
    """Check if a required directory exists."""
    if dirpath.exists() and dirpath.is_dir():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} (missing: {dirpath})")
        return False


def main():
    """Check if the repository is properly set up."""
    print("🎙️ Podcast Transcriber GitHub Action Setup Check")
    print("=" * 60)
    
    repo_root = Path(".")
    all_good = True
    
    # Check core files
    core_files = [
        (repo_root / "main.py", "Core transcription script"),
        (repo_root / "github_action_processor.py", "GitHub Action processor"),
        (repo_root / "postprocess_transcript.py", "AI post-processing script"),
        (repo_root / "pyproject.toml", "Python dependencies configuration"),
    ]
    
    print("\n📄 Core Files:")
    for filepath, description in core_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check GitHub configuration
    github_files = [
        (repo_root / ".github" / "ISSUE_TEMPLATE" / "podcast-transcription-request.yml", "Issue template"),
        (repo_root / ".github" / "workflows" / "transcribe-podcast.yml", "GitHub Action workflow"),
    ]
    
    print("\n🔧 GitHub Configuration:")
    for filepath, description in github_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check directories
    directories = [
        (repo_root / ".github", ".github directory"),
        (repo_root / ".github" / "ISSUE_TEMPLATE", "Issue templates directory"),
        (repo_root / ".github" / "workflows", "GitHub workflows directory"),
    ]
    
    print("\n📁 Required Directories:")
    for dirpath, description in directories:
        if not check_directory_exists(dirpath, description):
            all_good = False
    
    # Check if running in a git repository
    print("\n🔍 Repository Status:")
    if (repo_root / ".git").exists():
        print("✅ Git repository detected")
    else:
        print("❌ Not a git repository (run 'git init' first)")
        all_good = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 Setup Complete!")
        print("\nYour repository is ready for podcast transcription!")
        print("\nNext steps:")
        print("1. Push your changes to GitHub")
        print("2. Go to your repository's Issues tab")
        print("3. Create a new issue using the 'Podcast Transcription Request' template")
        print("4. Fill in the form with your podcast details")
        print("5. Submit and watch the magic happen! ✨")
    else:
        print("❌ Setup Incomplete")
        print("\nPlease fix the missing files/directories above.")
        print("You may need to run the setup process again.")
    
    print("\n" + "=" * 60)
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())