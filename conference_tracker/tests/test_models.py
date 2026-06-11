"""
Unit tests for Event model methods in models.py.

This module tests individual model functions like `to_dict` and `__repr__`
using standard unittest structures.
"""

import unittest
from datetime import datetime
from models import Event


class EventModelTestCase(unittest.TestCase):
    """Test suite targeting individual Event model methods."""

    def test_event_to_dict_method(self):
        """Test that to_dict correctly serializes Event properties to a dictionary."""
        start_time = datetime(2026, 6, 12, 10, 0)
        end_time = datetime(2026, 6, 12, 11, 30)

        event = Event(
            id=42,
            title="Design Thinking in the AI Era",
            description="Exploring the intersection of modern UX design and AI reasoning.",
            speaker="Elena Rostova",
            start_time=start_time,
            end_time=end_time,
            location="Room 304",
            category="Workshop",
        )

        event_dict = event.to_dict()

        # Validate structure and key/value correctness
        self.assertEqual(event_dict["id"], 42)
        self.assertEqual(event_dict["title"], "Design Thinking in the AI Era")
        self.assertEqual(event_dict["description"], "Exploring the intersection of modern UX design and AI reasoning.")
        self.assertEqual(event_dict["speaker"], "Elena Rostova")
        self.assertEqual(event_dict["start_time"], start_time.isoformat())
        self.assertEqual(event_dict["end_time"], end_time.isoformat())
        self.assertEqual(event_dict["location"], "Room 304")
        self.assertEqual(event_dict["category"], "Workshop")

    def test_event_repr_method(self):
        """Test that __repr__ provides a readable developer representation."""
        event = Event(
            title="Sleek UI with CSS Glassmorphism",
            speaker="Marcus Aurelius",
        )

        expected_repr = "<Event Sleek UI with CSS Glassmorphism by Marcus Aurelius>"
        self.assertEqual(repr(event), expected_repr)


if __name__ == "__main__":
    unittest.main()
