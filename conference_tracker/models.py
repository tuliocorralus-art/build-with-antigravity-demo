"""
Database models for the Conference Event Tracker.

This module defines the database models using Flask-SQLAlchemy.
All models follow the PEP 8 style guide and contain detailed docstrings.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize db instance (to be bound to the Flask app in app.py)
db = SQLAlchemy()


class Event(db.Model):
    """
    Represents a conference session, workshop, or event.

    Attributes:
        id (int): Primary key.
        title (str): The name/title of the conference event.
        description (str): Detailed description of what the event is about.
        speaker (str): Name of the speaker or moderator.
        start_time (datetime): Start timestamp of the event.
        end_time (datetime): End timestamp of the event.
        location (str): The physical or virtual room/venue location.
        category (str): Event category (e.g., Keynote, Workshop, Technical).
    """

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    speaker = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """
        Convert the model instance into a dictionary.

        Returns:
            dict: JSON-serializable representation of the Event.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "speaker": self.speaker,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "location": self.location,
            "category": self.category,
        }

    def __repr__(self):
        return f"<Event {self.title} by {self.speaker}>"
