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

def detectar(juego, contexto_usuario, transcripcion_path):
    print("Detectando clips con GPT...")

    with open(transcripcion_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transcripcion_texto = ""
    for segmento in data["segments"]:
        transcripcion_texto += f"[{segmento['start']:.1f}s - {segmento['end']:.1f}s] {segmento['text']}\n"

    prompt_sistema = f"""Eres un experto analizando audio transcrito de sesiones de {juego} para encontrar momentos que valen la pena convertir en clips de TikTok y YouTube Shorts.

El usuario te va a explicar qué patrones de habla o palabras clave indican un momento importante en su juego específico. Usa ESO como tu única guía, no asumas nada por tu cuenta sobre el juego:

CONTEXTO Y PALABRAS CLAVE DEL USUARIO:
{contexto_usuario}

IMPORTANTE:
- Solo marca como clip los momentos que coincidan con lo que el usuario describió arriba.
- Si una palabra clave aparece pero sin el contexto que el usuario indicó, NO es clip.
- Agrupa momentos cercanos en un solo clip.
- El clip debe empezar 7 segundos antes del evento y terminar 7 segundos después.

Devuelve ÚNICAMENTE un JSON válido sin texto adicional:
[
  {{
    "inicio": 45,
    "fin": 75,
    "motivo": "descripción breve"
  }}
]"""

    respuesta = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Analiza esta transcripción y encuentra los mejores momentos:\n\n{transcripcion_texto}"}
        ]
    )

    resultado_texto = respuesta.choices[0].message.content
    resultado_limpio = resultado_texto.replace("```json", "").replace("```", "").strip()
    resultado_json = json.loads(resultado_limpio)

    print(f"✓ {len(resultado_json)} clips detectados")
    for clip in resultado_json:
        print(f"  {clip['inicio']}s - {clip['fin']}s | {clip['motivo']}")

    return resultado_json