#!/usr/bin/env python3
"""Extract a thumbnail from a video file using ffmpeg."""
import subprocess
import sys
import os

def extract_thumbnail(video_path: str, video_id: str) -> str:
    output_path = f"/tmp/{video_id}.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-ss", "1",
        "-vframes", "1",
        "-q:v", "2",
        output_path,
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")

    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <video_path> <video_id>", file=sys.stderr)
        sys.exit(1)
    video_path, video_id = sys.argv[1], sys.argv[2]
    out = extract_thumbnail(video_path, video_id)
    print(f"Thumbnail saved to: {out}")
