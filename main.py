import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from controller import Controller

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Note App Pro")
    window.resize(700, 900)

    Controller(window)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()