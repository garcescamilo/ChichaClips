import subprocess
import os

def extraer_audio(video_path, temp_dir="temp"):
    nombre_base = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(temp_dir, f"{nombre_base}.wav")

    print("Extrayendo audio del video...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ], capture_output=True)
    print(f"✓ Audio extraído: {audio_path}")

    return audio_path