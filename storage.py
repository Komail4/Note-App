import json
import os
from models.note import Note

class NoteStorage:
    """Handles saving and loading notes from a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        dirpath = os.path.dirname(file_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

    def load_notes(self) -> list[Note]:
        """Load all notes from JSON file."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            notes_data = data.get("notes", [])
            if not isinstance(notes_data, list):
                return []
            return [Note.from_dict(n) for n in notes_data]
        except (json.JSONDecodeError, OSError):
            return []

    def save_notes(self, notes: list[Note]) -> None:
        """Save all notes to JSON file atomically where possible."""
        data = {"notes": [n.to_dict() for n in notes]}
        dirpath = os.path.dirname(self.file_path)
        temp_path = self.file_path + ".tmp"
        try:
            # ensure dir exists (defensive)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            os.replace(temp_path, self.file_path)  # atomic on many OSes
        except OSError:
            # Clean up temp file if present
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass
            raise