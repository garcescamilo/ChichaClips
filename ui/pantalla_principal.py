from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog
from ui.pantalla_progreso import PantallaProgreso

class PantallaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClipAI")
        self.setMinimumSize(500, 600)

        self.video_path = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("🎮 ClipAI")
        layout.addWidget(titulo)

        self.label_video = QLabel("Ningún video seleccionado")
        layout.addWidget(self.label_video)

        self.boton_video = QPushButton("Seleccionar video")
        self.boton_video.clicked.connect(self.seleccionar_video)
        layout.addWidget(self.boton_video)

        layout.addWidget(QLabel("Juego:"))
        self.input_juego = QLineEdit()
        layout.addWidget(self.input_juego)

        layout.addWidget(QLabel("Contexto / palabras clave:"))
        self.input_contexto = QTextEdit()
        layout.addWidget(self.input_contexto)

        self.boton_analizar = QPushButton("Analizar Video")
        self.boton_analizar.clicked.connect(self.iniciar_analisis)
        layout.addWidget(self.boton_analizar)

    def seleccionar_video(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Selecciona un video",
            "",
            "Videos (*.mp4 *.mkv *.avi *.mov)"
        )
        if ruta:
            self.video_path = ruta
            self.label_video.setText(f"Video: {ruta.split('/')[-1]}")


    def iniciar_analisis(self):
        juego = self.input_juego.text()
        contexto = self.input_contexto.toPlainText()

        if not self.video_path:
            self.label_video.setText("⚠️ Primero selecciona un video")
            return

        if not juego or not contexto:
            self.label_video.setText("⚠️ Completa el juego y el contexto")
            return

        self.pantalla_progreso = PantallaProgreso(self.video_path, juego, contexto)
        self.pantalla_progreso.show()
        self.close()