from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal
import os
import cv2

class PantallaResultados(QWidget):
    volver_inicio = Signal()

    def __init__(self, clips):
        super().__init__()
        self.setWindowTitle("Chicha Clips - Resultados")
        self.setMinimumSize(800, 400)

        self.clips = clips

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(16)
        self.setLayout(layout_principal)

        titulo = QLabel(f"🎬 {len(clips)} clips detectados")
        titulo.setObjectName("titulo")
        layout_principal.addWidget(titulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedHeight(160)
        layout_principal.addWidget(scroll)

        contenedor = QWidget()
        self.layout_fila = QHBoxLayout()
        self.layout_fila.setSpacing(14)
        self.layout_fila.setContentsMargins(0, 0, 0, 0)
        contenedor.setLayout(self.layout_fila)
        scroll.setWidget(contenedor)

        for clip in clips:
            tarjeta = self.crear_tarjeta(clip)
            self.layout_fila.addWidget(tarjeta)

        self.layout_fila.addStretch()
        layout_principal.addStretch()

        self.boton_volver = QPushButton("← Analizar otro video")
        self.boton_volver.setObjectName("boton_secundario")
        self.boton_volver.clicked.connect(self.volver_a_inicio)
        layout_principal.addWidget(self.boton_volver)

        self.boton_carpeta = QPushButton("Abrir carpeta de clips")
        self.boton_carpeta.setObjectName("boton_secundario")
        self.boton_carpeta.clicked.connect(self.abrir_carpeta)
        layout_principal.addWidget(self.boton_carpeta)

    def crear_tarjeta(self, clip):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setFixedWidth(170)
        layout_tarjeta = QVBoxLayout()
        layout_tarjeta.setContentsMargins(6, 6, 6, 6)
        layout_tarjeta.setSpacing(0)
        tarjeta.setLayout(layout_tarjeta)

        boton_thumb = QPushButton()
        boton_thumb.setObjectName("thumb")
        boton_thumb.setFixedSize(158, 90)
        boton_thumb.setCursor(Qt.PointingHandCursor)

        pixmap = self.generar_thumbnail(clip["archivo"])
        if pixmap:
            boton_thumb.setIcon(pixmap)
            boton_thumb.setIconSize(boton_thumb.size())

        boton_thumb.clicked.connect(lambda: self.reproducir_clip(clip["archivo"]))
        layout_tarjeta.addWidget(boton_thumb)

        return tarjeta

    def generar_thumbnail(self, archivo_video):
        cap = cv2.VideoCapture(archivo_video)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        alto, ancho, canales = frame_rgb.shape
        bytes_por_linea = canales * ancho

        imagen_qt = QImage(frame_rgb.data, ancho, alto, bytes_por_linea, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(imagen_qt)
        pixmap = pixmap.scaled(158, 90, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        return pixmap

    def reproducir_clip(self, archivo):
        os.startfile(archivo)

    def abrir_carpeta(self):
        os.startfile("clips")

    def volver_a_inicio(self):
        from ui.pantalla_principal import PantallaPrincipal
        self.pantalla_principal = PantallaPrincipal()
        self.pantalla_principal.show()
        self.close()