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
        # reuse existing layout if present, otherwise create and set one
        layout = self.layout() or QVBoxLayout()
        if self.layout() is None:
            self.setLayout(layout)

        # clear existing widgets from the layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            w = item.widget()
            if w:
                w.deleteLater()
            layout.removeItem(item)

        data = self.controller.load_data()
        if data is None:
            welcome_label = QLabel("Welcome to Note App!\nNo data found. Please create a new note.")
            layout.addWidget(welcome_label)
            return

        welcome_label = QLabel("Welcome to Note App!")
        layout.addWidget(welcome_label)
        count = len(data.get("notes", []))

        for note in reversed(data.get("notes", [])):
            title = f"""{note['date']}
📄 {note['title']}"""
            note_button = QPushButton(title)
            # fix closure: bind current note to default arg
            note_button.clicked.connect(lambda n=note: self.controller.open_notes_page(n['id']))
            note_button.setStyleSheet("text-align: left; padding: 10px;")
            layout.addWidget(note_button)

        add_btn = QPushButton("➕ Add Note")
        add_btn.clicked.connect(lambda: self.controller.add_new_note())

        layout.addStretch()
        layout.addWidget(add_btn)
    
    def refresh(self):
        self.init_ui()

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
        data = self.load_data()
        if data is None:
            return
        new_id = max([note['id'] for note in data['notes']], default=0) + 1
        new_note = {
            "id": new_id,
            "title": "New Note",
            "content": "",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data['notes'].append(new_note)
        self.save_data(data)
        self.start_page.refresh()

# ----------------- Run App -----------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()