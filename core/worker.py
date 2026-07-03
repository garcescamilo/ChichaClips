from PySide6.QtCore import QThread, Signal
from core.extraer_audio import extraer_audio
from core.transcribir import transcribir
from core.detectar_clips import detectar
from core.cortar_clips import cortar
import os
import shutil

class PipelineWorker(QThread):
    progreso = Signal(str)
    terminado = Signal(list)
    error = Signal(str)

    def __init__(self, video_path, juego, contexto):
        super().__init__()
        self.video_path = video_path
        self.juego = juego
        self.contexto = contexto

    def run(self):
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            self.progreso.emit("Extrayendo audio...")
            audio_path = extraer_audio(self.video_path, temp_dir)

            self.progreso.emit("Transcribiendo audio...")
            transcripcion_path = transcribir(audio_path, temp_dir)

            self.progreso.emit("Detectando clips...")
            clips = detectar(self.juego, self.contexto, transcripcion_path)

            self.progreso.emit("Cortando clips...")
            clips_finales = cortar(self.video_path, clips)

            self.terminado.emit(clips_finales)

        except Exception as e:
            self.error.emit(str(e))

        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)