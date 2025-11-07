from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
import datetime

class NotesPage(QWidget):
    """Page for editing a single note."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setLayout(QVBoxLayout())

    def refresh(self):
        self.clear_layout()
        layout = self.layout()
        note = self.controller.current_note

        if not note:
            layout.addWidget(QLabel("Note not found."))
            back = QPushButton("🔙 Back")
            back.clicked.connect(self.controller.back_to_start)
            layout.addWidget(back)
            return

        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        title_edit = QLineEdit(note.title)
        title_edit.textChanged.connect(lambda text: setattr(note, "title", text))
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_edit)
        layout.addLayout(title_layout)

        # Tags
        tag_layout = QHBoxLayout()
        tag_label = QLabel("Tags (comma-separated):")
        tag_edit = QLineEdit(", ".join(note.tags))
        tag_edit.textChanged.connect(lambda text: setattr(note, "tags", [t.strip() for t in text.split(",") if t.strip()]))
        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(tag_edit)
        layout.addLayout(tag_layout)

        # Content
        layout.addWidget(QLabel("Content:"))
        content_edit = QTextEdit(note.content)
        content_edit.textChanged.connect(lambda: setattr(note, "content", content_edit.toPlainText()))
        layout.addWidget(content_edit)

        # Info
        layout.addWidget(QLabel(f"🕒 Created: {note.date}"))
        layout.addWidget(QLabel(f"✏️ Last Edited: {note.last_edited}"))

        # Buttons
        save_btn = QPushButton("💾 Save Note")
        delete_btn = QPushButton("🗑 Delete Note")
        back_btn = QPushButton("🔙 Back")

        save_btn.clicked.connect(lambda: self.save_note(note))
        delete_btn.clicked.connect(lambda: self.delete_note(note))
        back_btn.clicked.connect(self.controller.back_to_start)

        layout.addWidget(save_btn)
        layout.addWidget(delete_btn)
        layout.addWidget(back_btn)
        layout.addStretch()

    def clear_layout(self):
        """Recursively clear all widgets and nested layouts from this page's layout."""
        def _clear(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item is None:
                    continue
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    child_layout = item.layout()
                    if child_layout is not None:
                        _clear(child_layout)
        layout = self.layout()
        if layout is not None:
            _clear(layout)

    def save_note(self, note):
        note.last_edited = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.controller.save_or_update(note)
        QMessageBox.information(self, "Saved", "✅ Note saved successfully!")
        self.controller.back_to_start()

    def delete_note(self, note):
        reply = QMessageBox.question(self, "Delete Note", "Are you sure you want to delete this note?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.delete_note(note)
            QMessageBox.information(self, "Deleted", "🗑 Note deleted.")
            self.controller.back_to_start()
