import sys
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

load_dotenv(resource_path(".env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribir(audio_path, temp_dir="temp"):
    print("Transcribiendo audio...")
    with open(audio_path, "rb") as audio_file:
        transcripcion = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            language="es"
        )

    nombre_base = os.path.splitext(os.path.basename(audio_path))[0]
    transcripcion_path = os.path.join(temp_dir, f"{nombre_base}_transcripcion.json")

    with open(transcripcion_path, "w", encoding="utf-8") as f:
        json.dump(transcripcion.model_dump(), f, ensure_ascii=False, indent=2)

    print(f"✓ Transcripción lista: {len(transcripcion.segments)} segmentos")
    return transcripcion_path