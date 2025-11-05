import sys
import os
import json
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt


# ----------------- Start Page -----------------
class StartPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setLayout(QVBoxLayout())
        self.refresh()

    def clear_layout(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh(self):
        self.clear_layout()
        layout = self.layout()

        data = self.controller.load_data()
        notes = data.get("notes", [])

        if not notes:
            layout.addWidget(QLabel("Welcome to Note App!\nNo notes found. Please create a new note."))
        else:
            layout.addWidget(QLabel("Welcome to Note App!"))
            for note in reversed(notes):
                if not isinstance(note, dict) or "id" not in note:
                    continue
                title = f"{note.get('date', '')}\n📄 {note.get('title', '<untitled>')}"
                btn = QPushButton(title)
                btn.setStyleSheet("text-align: left; padding: 10px;")
                btn.clicked.connect(lambda _, n=note: self.controller.open_notes_page(n))
                layout.addWidget(btn)

        add_btn = QPushButton("➕ Add Note")
        add_btn.clicked.connect(self.controller.add_new_note)
        layout.addStretch()
        layout.addWidget(add_btn)


# ----------------- Notes Page -----------------
class NotesPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setLayout(QVBoxLayout())

    def clear_layout(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh(self):
        self.clear_layout()
        layout = self.layout()

        note = self.controller.current_note
        if not note:
            layout.addWidget(QLabel("Note not found."))
            back_btn = QPushButton("🔙 Back to Notes List")
            back_btn.clicked.connect(self.controller.back_to_start)
            layout.addWidget(back_btn)
            return

        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        title_edit = QLineEdit(note.get("title", ""))
        title_edit.textChanged.connect(lambda text: note.update({"title": text}))
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_edit)
        layout.addLayout(title_layout)

        # Content
        content_label = QLabel("Content:")
        content_edit = QTextEdit()
        content_edit.setPlainText(note.get("content", ""))
        content_edit.textChanged.connect(lambda: note.update({"content": content_edit.toPlainText()}))
        layout.addWidget(content_label)
        layout.addWidget(content_edit)

        # Buttons
        save_btn = QPushButton("💾 Save Note")
        save_btn.clicked.connect(lambda: self.controller.save_note_changes(note))
        back_btn = QPushButton("🔙 Back to Notes List")
        back_btn.clicked.connect(self.controller.back_to_start)
        layout.addWidget(save_btn)
        layout.addWidget(back_btn)

        layout.addStretch()


# ----------------- Main Window -----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note App")
        self.setGeometry(200, 200, 700, 900)
        self.file_path = "Note app/data.json"
        self.current_note = None

        # Stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.start_page = StartPage(self)
        self.notes_page = NotesPage(self)
        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.notes_page)

        self.show_page("Start")

    # -------- Navigation --------
    def show_page(self, name):
        if name == "Start":
            self.start_page.refresh()
            self.stack.setCurrentWidget(self.start_page)
        elif name == "Notes":
            self.notes_page.refresh()
            self.stack.setCurrentWidget(self.notes_page)

    def back_to_start(self):
        self.current_note = None
        self.show_page("Start")

    def open_notes_page(self, note):
        """Open selected note"""
        self.current_note = note
        self.show_page("Notes")

    # -------- Data Handling --------
    def load_data(self):
        if not os.path.exists(self.file_path):
            return {"notes": []}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "notes" in data:
                return data
            if isinstance(data, list):
                return {"notes": data}
        except (json.JSONDecodeError, OSError):
            pass
        return {"notes": []}

    def save_data(self, data):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_note_changes(self, updated_note):
        """Replace or add a note"""
        data = self.load_data()
        notes = data.get("notes", [])
        for i, n in enumerate(notes):
            if n.get("id") == updated_note.get("id"):
                notes[i] = updated_note
                break
        else:
            notes.append(updated_note)
        self.save_data({"notes": notes})
        self.back_to_start()

    def add_new_note(self):
        data = self.load_data()
        notes = data.get("notes", [])
        new_id = max((n.get("id", 0) for n in notes), default=0) + 1
        new_note = {
            "id": new_id,
            "title": "New Note",
            "content": "",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        notes.append(new_note)
        self.save_data({"notes": notes})
        self.start_page.refresh()


# ----------------- Run App -----------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()