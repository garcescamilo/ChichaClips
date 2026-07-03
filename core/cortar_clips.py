import os
import subprocess

OUTPUT_DIR = "clips"
SEGUNDOS_ANTES = 7
SEGUNDOS_DESPUES = 7

def cortar(video_path, clips):
    print("Cortando clips...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    clips_finales = []

    for i, clip in enumerate(clips):
        inicio = max(0, clip["inicio"] - SEGUNDOS_ANTES)
        fin = clip["fin"] + SEGUNDOS_DESPUES
        duracion = fin - inicio
        output_path = os.path.join(OUTPUT_DIR, f"clip_{i+1:02d}.mp4")

        subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(inicio),
            "-i", video_path,
            "-t", str(duracion),
            "-c", "copy",
            output_path
        ], capture_output=True)

        print(f"  ✓ {output_path}")

        clip_info = dict(clip)
        clip_info["archivo"] = output_path
        clips_finales.append(clip_info)

    print(f"\n✓ {len(clips)} clips en '{OUTPUT_DIR}/'")
    return clips_finales