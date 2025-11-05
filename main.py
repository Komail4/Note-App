import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout, QLineEdit, QTextEdit, QListWidget, QDialog,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt
import json
import os
import datetime

# ----------------- Pages -----------------
class StartPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        data = self.controller.load_data()
        if data is None:
            welcome_label = QLabel("Welcome to Note App!\nNo data found. Please create a new note.")
            layout.addWidget(welcome_label)
            self.setLayout(layout)
            return
        
        welcome_label = QLabel("Welcome to Note App!")
        layout.addWidget(welcome_label)
        count = len(data["notes"]) if "notes" in data else 0

        for i in range(count):
            note = data["notes"][i]
            title = f"""{note['date']}
📄 {note["title"]}"""
            note_button = QPushButton(title)
            note_button.clicked.connect(lambda: self.controller.open_notes_page(note['id']))
            note_button.setStyleSheet("text-align: left; padding: 10px;")
            layout.addWidget(note_button)

        add_btn = QPushButton("➕ Add Note")
        add_btn.clicked.connect(self.controller.add_new_note)

        layout.addStretch()
        layout.addWidget(add_btn)

        self.setLayout(layout)


class NotesPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)

# ----------------- Main Window -----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note App")
        self.setGeometry(200, 200, 700, 1000)

        self.file_path = "Note app/data.json"

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.start_page = StartPage(self)
        self.notes_page = NotesPage(self)

        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.notes_page)

        self.show_page("Start")

    def show_page(self, name):
        if name == "Start":
            page = self.start_page
        elif name == "Notes":
            page = self.notes_page
        else:
            return
        
        self.stack.setCurrentWidget(page)
        
        if hasattr(page, "refresh") and callable(page.refresh):
            page.refresh()
    
    def save_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def load_data(self):
        if not os.path.exists(self.file_path):
            # messagebox.showerror("Error", "File did not found")
            print("File did not found")
            return None
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # messagebox.showerror("Error", "Data file not found.")
            print("Data file not found.")
            return None 
    
    def open_notes_page(self, id):
        self.show_page("Notes")

    def add_new_note(self):
        pass

# ----------------- Run App -----------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()