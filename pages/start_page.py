from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt

class StartPage(QWidget):
    """Page that lists all notes and allows search or adding new ones."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Main layout for the page (static)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Search bar (persistent)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search notes...")
        # Connect after refresh so update_list has up-to-date notes (we'll connect in refresh)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Create a scroll area to hold the notes list so it can scroll when large
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # The scroll area's content must be a widget with a layout
        self.scroll_content = QWidget()
        self.note_container = QVBoxLayout()  # this holds note buttons
        self.note_container.setContentsMargins(0, 0, 0, 0)
        self.note_container.setSpacing(6)
        self.scroll_content.setLayout(self.note_container)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Add button (persistent)
        self.add_btn = QPushButton("➕ Add Note")
        self.add_btn.clicked.connect(self.controller.add_new_note)
        main_layout.addWidget(self.add_btn)

        # Initial population
        self.refresh()

    def clear_layout(self, layout):
        """Recursively clear all widgets and nested layouts from the given layout."""
        if layout is None:
            return

        def _clear(l):
            while l.count():
                item = l.takeAt(0)
                if item is None:
                    continue
                widget = item.widget()
                if widget is not None:
                    # remove widget from layout and schedule deletion
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    child_layout = item.layout()
                    if child_layout is not None:
                        _clear(child_layout)

        _clear(layout)

    def refresh(self):
        """Refresh the visible notes list. Keeps the page structure intact."""
        notes = self.controller.storage.load_notes() or []

        # (re)connect search to current notes; disconnect previous signal first to avoid duplicate calls
        try:
            self.search_input.textChanged.disconnect()
        except Exception:
            pass
        self.search_input.textChanged.connect(lambda text: self.update_list(notes, text))

        # If no notes, show a welcome message inside the scroll area
        if not notes:
            self.clear_layout(self.note_container)
            welcome = QLabel("Welcome to Note App!\nNo notes found. Please create a new note.")
            welcome.setAlignment(Qt.AlignCenter)
            self.note_container.addStretch()
            self.note_container.addWidget(welcome)
            self.note_container.addStretch()
            return

        # Otherwise populate the notes into the note_container
        self.display_notes(notes)

    def display_notes(self, notes):
        """Display notes list inside the scroll area's content layout."""
        # Clear previous buttons
        self.clear_layout(self.note_container)

        # Add a button per note (newest first)
        for note in reversed(notes):
            title = f"{note.date}   📄 {note.title}"
            btn = QPushButton(title)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("text-align: left; padding: 10px;")
            # bind note as default arg so lambda captures the correct one
            btn.clicked.connect(lambda _, n=note: self.controller.open_note_page(n))
            self.note_container.addWidget(btn)

        # Push items to the top
        self.note_container.addStretch()

    def update_list(self, all_notes, keyword):
        """Filter notes by keyword and refresh the display (simple title/content/tags match)."""
        kw = (keyword or "").strip().lower()
        if not kw:
            filtered = all_notes
        else:
            filtered = []
            for n in all_notes:
                if kw in (n.title or "").lower() or kw in (n.content or "").lower() or any(kw in t.lower() for t in (n.tags or [])):
                    filtered.append(n)
        self.display_notes(filtered)