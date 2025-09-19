#!/usr/bin/env python3
"""
Pre-commit verification script for the Podcast Transcriber GitHub Action.
Run this before pushing to ensure everything is set up correctly.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and return True if successful."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False


def check_python_syntax():
    """Check Python syntax of all Python files."""
    python_files = [
        "main.py",
        "github_action_processor.py", 
        "postprocess_transcript.py",
        "test_processor.py",
        "setup_check.py"
    ]
    
    all_good = True
    for file in python_files:
        if Path(file).exists():
            if not run_command(f"python -m py_compile {file}", f"Syntax check for {file}"):
                all_good = False
        else:
            print(f"❌ Missing file: {file}")
            all_good = False
    
    return all_good


def check_yaml_syntax():
    """Check YAML syntax of GitHub workflow files."""
    import yaml
    
    yaml_files = [
        ".github/ISSUE_TEMPLATE/podcast-transcription-request.yml",
        ".github/workflows/transcribe-podcast.yml"
    ]
    
    all_good = True
    for file in yaml_files:
        filepath = Path(file)
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
                print(f"✅ YAML syntax check for {file} - Success")
            except yaml.YAMLError as e:
                print(f"❌ YAML syntax check for {file} - Failed: {e}")
                all_good = False
        else:
            print(f"❌ Missing file: {file}")
            all_good = False
    
    return all_good


def check_dependencies():
    """Check if all dependencies are properly installed."""
    return run_command("uv sync --check", "Dependency check")


def run_tests():
    """Run the test suite."""
    return run_command("uv run python test_processor.py", "Test suite")


def check_git_status():
    """Check git status and suggest next steps."""
    print("\n📋 Git Status:")
    
    if not Path(".git").exists():
        print("❌ Not a git repository. Run 'git init' first.")
        return False
    
    # Check for uncommitted changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📝 Uncommitted changes detected:")
        print(result.stdout)
        print("\n💡 Next steps:")
        print("   1. Review your changes: git status")
        print("   2. Add files: git add .")
        print("   3. Commit: git commit -m 'Set up podcast transcriber'")
        print("   4. Push to GitHub: git push origin main")
    else:
        print("✅ Working directory is clean")
        print("\n💡 If you haven't pushed yet:")
        print("   git push origin main")
    
    return True


def main():
    """Run all verification checks."""
    print("🎙️ Podcast Transcriber Pre-Commit Verification")
    print("=" * 60)
    
    checks = [
        ("Python syntax validation", check_python_syntax),
        ("YAML syntax validation", check_yaml_syntax),
        ("Dependency verification", check_dependencies),
        ("Test suite", run_tests),
        ("Git status check", check_git_status),
    ]
    
    all_passed = True
    
    for description, check_func in checks:
        print(f"\n📋 {description}:")
        print("-" * 40)
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 All checks passed!")
        print("\nYour Podcast Transcriber is ready for deployment! 🚀")
        print("\n📋 Final checklist:")
        print("   ✅ Code syntax is valid")
        print("   ✅ Dependencies are installed")
        print("   ✅ Tests are passing")
        print("   ✅ Configuration files are valid")
        print("\n🚀 Ready to push to GitHub!")
    else:
        print("❌ Some checks failed!")
        print("\nPlease fix the issues above before proceeding.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())