import sys
from PySide6.QtWidgets import QApplication
from ui.pantalla_principal import PantallaPrincipal

app = QApplication(sys.argv)
ventana = PantallaPrincipal()
ventana.show()
sys.exit(app.exec())