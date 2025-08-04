# SubGen - Whisper Subtitle Generator

A simple Python CLI tool that uses OpenAI's Whisper to automatically generate subtitles for video files in a directory (recursively).

## Features

- Recursively scans directories for video files
- Generates SRT subtitle files using Whisper
- Supports multiple Whisper models (tiny, base, small, medium, large)
- Skips files that already have subtitles (optional)
- Dry-run mode to preview what will be processed
- Comprehensive error handling and progress reporting

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable (optional):
```bash
chmod +x subgen.py
```

## Usage

Basic usage:
```bash
python subgen.py /path/to/video/directory
```

With options:
```bash
# Use a different Whisper model
python subgen.py /path/to/videos --model small

# Skip videos that already have subtitle files
python subgen.py /path/to/videos --skip-existing

# Preview what will be processed without generating subtitles
python subgen.py /path/to/videos --dry-run

# Combine options
python subgen.py /path/to/videos --model medium --skip-existing
```

## Command Line Options

- `directory`: Path to directory containing video files (required)
- `--model, -m`: Whisper model to use (tiny, base, small, medium, large, large-v1, large-v2, large-v3) - default: large-v3
- `--skip-existing, -s`: Skip videos that already have subtitle files
- `--dry-run, -n`: Show what would be processed without generating subtitles

## Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MKV (.mkv)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)
- M4V (.m4v)
- 3GP (.3gp)
- OGV (.ogv)
- TS (.ts)
- MTS (.mts)
- M2TS (.m2ts)

## Output

Subtitle files are saved as `.srt` files in the same directory as the original video files, with the same filename as the video.

For example:
- `movie.mp4` → `movie.srt`
- `documentary.mkv` → `documentary.srt`

## Whisper Models

Different models offer trade-offs between speed and accuracy:

- `tiny`: Fastest, least accurate
- `base`: Good balance
- `small`: Better accuracy, slower
- `medium`: High accuracy, much slower
- `large`: Best accuracy, slowest
- `large-v1`: Enhanced large model
- `large-v2`: Improved large model
- `large-v3`: Latest and most accurate (default)

## Requirements

- Python 3.7+
- OpenAI Whisper
- FFmpeg (required by Whisper)

## Notes

- The first run may take longer as Whisper downloads the selected model
- Processing time depends on video length and selected model
- Ensure you have sufficient disk space for the model and temporary files
