import datetime

class Note:
    """Represents a single note object."""

    def __init__(self, note_id: int, title: str, content: str, date: str, tags=None, last_edited=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.date = date
        self.tags = tags or []
        self.last_edited = last_edited or date

    def to_dict(self) -> dict:
        """Convert note to dictionary for saving."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date": self.date,
            "tags": self.tags,
            "last_edited": self.last_edited
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Note object from a dictionary."""
        return cls(
            note_id=data.get("id", 0),
            title=data.get("title", ""),
            content=data.get("content", ""),
            date=data.get("date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            tags=data.get("tags", []),
            last_edited=data.get("last_edited")
        )
