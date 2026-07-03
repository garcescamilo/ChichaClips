from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from core.worker import PipelineWorker

class PantallaProgreso(QWidget):
    def __init__(self, video_path, juego, contexto):
        super().__init__()
        self.setWindowTitle("Chicha Clips - Procesando")
        self.setMinimumSize(500, 350)
        self.setMaximumSize(500, 350)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        self.setLayout(layout)

        titulo = QLabel("Procesando tu video...")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        layout.addSpacing(20)

        self.pasos = {
            "audio": QLabel("⬜  Extrayendo audio"),
            "transcribir": QLabel("⬜  Transcribiendo con Whisper"),
            "detectar": QLabel("⬜  Detectando clips con GPT"),
            "cortar": QLabel("⬜  Cortando clips"),
        }

        for label in self.pasos.values():
            label.setObjectName("paso")
            layout.addWidget(label)

        layout.addSpacing(20)

        self.barra = QProgressBar()
        self.barra.setRange(0, 4)
        self.barra.setValue(0)
        self.barra.setTextVisible(False)
        layout.addWidget(self.barra)

        self.pasos_completados = 0

        self.worker = PipelineWorker(video_path, juego, contexto)
        self.worker.progreso.connect(self.actualizar_estado)
        self.worker.terminado.connect(self.proceso_terminado)
        self.worker.error.connect(self.proceso_error)
        self.worker.start()

    def actualizar_estado(self, texto):
        mapa = {
            "Extrayendo audio...": "audio",
            "Transcribiendo audio...": "transcribir",
            "Detectando clips...": "detectar",
            "Cortando clips...": "cortar",
        }

        clave = mapa.get(texto)
        if clave:
            if self.pasos_completados > 0:
                claves = list(self.pasos.keys())
                paso_anterior = claves[self.pasos_completados - 1]
                self.pasos[paso_anterior].setText(
                    self.pasos[paso_anterior].text().replace("⏳", "✅")
                )

            self.pasos[clave].setText(
                self.pasos[clave].text().replace("⬜", "⏳")
            )

            self.pasos_completados += 1
            self.barra.setValue(self.pasos_completados)

    def proceso_terminado(self, clips):
        for label in self.pasos.values():
            if "⏳" in label.text():
                label.setText(label.text().replace("⏳", "✅"))

        self.barra.setValue(4)

        from ui.pantalla_resultados import PantallaResultados
        self.pantalla_resultados = PantallaResultados(clips)
        self.pantalla_resultados.show()
        self.close()

    def proceso_error(self, mensaje):
        for label in self.pasos.values():
            if "⏳" in label.text():
                label.setText(label.text().replace("⏳", "❌"))
        self.barra.setValue(0)

        error_label = self.findChild(QLabel, "error")
        if not error_label:
            from PySide6.QtWidgets import QLabel
            error = QLabel(f"Error: {mensaje}")
            error.setObjectName("error")
            error.setStyleSheet("color: #e05252;")
            self.layout().addWidget(error)