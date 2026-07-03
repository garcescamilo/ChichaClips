import sys
import os
from PySide6.QtWidgets import QApplication
from ui.pantalla_principal import PantallaPrincipal

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = QApplication(sys.argv)

with open(resource_path("ui/estilo.qss"), "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())

ventana = PantallaPrincipal()
ventana.show()
sys.exit(app.exec())