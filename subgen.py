#!/usr/bin/env python3
"""
SubGen - A CLI tool to generate subtitles for video files using Whisper
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Set

# Common video file extensions
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
    '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts'
}

def find_video_files(directory: Path) -> List[Path]:
    """
    Recursively find all video files in the given directory.
    
    Args:
        directory: Path to the directory to search
        
    Returns:
        List of Path objects for video files found
    """
    video_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in VIDEO_EXTENSIONS:
                    video_files.append(file_path)
    except PermissionError as e:
        print(f"Warning: Permission denied accessing {e.filename}")
    except Exception as e:
        print(f"Error scanning directory: {e}")
        
    return video_files

def check_whisper_installed() -> bool:
    """
    Check if Whisper CLI is installed and available.
    
    Returns:
        True if Whisper is available, False otherwise
    """
    try:
        result = subprocess.run(['whisper', '--help'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def generate_subtitle(video_path: Path, model: str = "large-v3") -> bool:
    """
    Generate subtitle file for a video using Whisper.
    
    Args:
        video_path: Path to the video file
        model: Whisper model to use (tiny, base, small, medium, large)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Whisper will automatically create subtitle files in the same directory
        # with the same name as the video file
        cmd = [
            'whisper',
            str(video_path),
            '--model', model,
            '--output_dir', str(video_path.parent),
            '--output_format', 'srt'
        ]
        
        print(f"Processing: {video_path.name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Generated subtitles for: {video_path.name}")
            return True
        else:
            print(f"✗ Failed to generate subtitles for: {video_path.name}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {video_path.name}: {e}")
        return False

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Generate subtitles for video files using Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/videos
  %(prog)s /path/to/videos --model small
  %(prog)s /path/to/videos --model medium --skip-existing
        """
    )
    
    parser.add_argument(
        'directory',
        help='Directory containing video files (searched recursively)'
    )
    
    parser.add_argument(
        '--model', '-m',
        default='large-v3',
        choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v1', 'large-v2', 'large-v3'],
        help='Whisper model to use (default: large-v3)'
    )
    
    parser.add_argument(
        '--skip-existing', '-s',
        action='store_true',
        help='Skip videos that already have subtitle files'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be processed without actually generating subtitles'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
        
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory")
        sys.exit(1)
    
    # Check if Whisper is installed
    if not args.dry_run and not check_whisper_installed():
        print("Error: Whisper CLI is not installed or not in PATH")
        print("Install it with: pip install openai-whisper")
        sys.exit(1)
    
    # Find video files
    print(f"Scanning for video files in: {directory}")
    video_files = find_video_files(directory)
    
    if not video_files:
        print("No video files found")
        sys.exit(0)
    
    print(f"Found {len(video_files)} video file(s)")
    
    # Filter out files that already have subtitles if requested
    if args.skip_existing:
        filtered_files = []
        for video_file in video_files:
            subtitle_file = video_file.with_suffix('.srt')
            if not subtitle_file.exists():
                filtered_files.append(video_file)
            else:
                print(f"Skipping {video_file.name} (subtitle already exists)")
        video_files = filtered_files
        
        if not video_files:
            print("All video files already have subtitles")
            sys.exit(0)
    
    # Show what will be processed
    print(f"\nWill process {len(video_files)} video file(s) with model '{args.model}':")
    for video_file in video_files:
        print(f"  - {video_file}")
    
    if args.dry_run:
        print("\nDry run complete - no subtitles were generated")
        sys.exit(0)
    
    # Confirm processing
    if len(video_files) > 1:
        response = input(f"\nProceed with generating subtitles? [y/N]: ")
        if response.lower() not in ['y', 'yes']:
            print("Cancelled")
            sys.exit(0)
    
    # Process video files
    print(f"\nGenerating subtitles using Whisper model '{args.model}'...")
    successful = 0
    failed = 0
    
    for video_file in video_files:
        if generate_subtitle(video_file, args.model):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print(f"\nCompleted processing {len(video_files)} video file(s)")
    print(f"✓ Successful: {successful}")
    if failed > 0:
        print(f"✗ Failed: {failed}")
    
    sys.exit(0 if failed == 0 else 1)

if __name__ == '__main__':
    main()
