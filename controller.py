from PyQt5.QtWidgets import QStackedWidget
from pages.start_page import StartPage
from pages.notes_page import NotesPage
from storage import NoteStorage
from models.note import Note
import datetime

class Controller:
    """Main controller that connects pages and handles logic."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.storage = NoteStorage("data/data.json")
        self.stack = QStackedWidget()
        main_window.setCentralWidget(self.stack)

        self.start_page = StartPage(self)
        self.notes_page = NotesPage(self)
        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.notes_page)

        self.current_note = None
        self.show_page("Start")

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

    def open_note_page(self, note):
        self.current_note = note
        self.show_page("Notes")

    def add_new_note(self):
        notes = self.storage.load_notes()
        new_id = max((n.id for n in notes), default=0) + 1
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_note = Note(new_id, "New Note", "", now)
        notes.append(new_note)
        self.storage.save_notes(notes)
        self.current_note = new_note
        self.show_page("Notes")

    def save_or_update(self, note):
        notes = self.storage.load_notes()
        for i, n in enumerate(notes):
            if n.id == note.id:
                notes[i] = note
                break
        else:
            notes.append(note)
        self.storage.save_notes(notes)

    def delete_note(self, note):
        notes = [n for n in self.storage.load_notes() if n.id != note.id]
        self.storage.save_notes(notes)
