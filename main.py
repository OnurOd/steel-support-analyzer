import sys
import os

# Add the project root to Python path so "src" is importable
sys.path.append(os.path.dirname(__file__))

from src.gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
