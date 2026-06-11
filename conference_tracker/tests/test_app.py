"""
Unit and Integration Tests for OmniEvent Conference Tracker.

This module provides thorough test coverage for routing, schema logic,
database seeding, and form validation rules.
"""

import os
import unittest
from datetime import datetime, timedelta
from app import app, db, Event


class OmniEventTestCase(unittest.TestCase):
    """Test suite for validating backend Flask logic and data persistence."""

    def setUp(self):
        """Set up a temporary in-memory database and test client before each test."""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            # Insert direct mock data for controlled testing
            self.event1 = Event(
                title="AI Testing Best Practices",
                description="Master unit testing in Flask and SQLAlchemy projects.",
                speaker="Tess Runner",
                start_time=datetime.utcnow() + timedelta(hours=1),
                end_time=datetime.utcnow() + timedelta(hours=2),
                location="Virtual Room 1",
                category="Technical",
            )
            db.session.add(self.event1)
            db.session.commit()

    def tearDown(self):
        """Clean up database and context after each test."""
        with app.app_context():
            db.drop_all()

    def test_dashboard_status_and_content(self):
        """Verify that the home page loads successfully and lists events."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        content = response.data.decode("utf-8")
        self.assertIn("OmniEvent", content)
        self.assertIn("AI Testing Best Practices", content)
        self.assertIn("Tess Runner", content)

    def test_api_events_endpoint(self):
        """Verify API returns valid serializable JSON data."""
        response = self.client.get("/api/events")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "AI Testing Best Practices")
        self.assertEqual(data[0]["speaker"], "Tess Runner")
        self.assertEqual(data[0]["category"], "Technical")

    def test_add_event_form_view(self):
        """Verify that the schedule event page loads successfully."""
        response = self.client.get("/add-event")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Schedule New Session", response.data.decode("utf-8"))

    def test_add_event_success(self):
        """Verify successful insertion of valid event data via POST form submission."""
        start_time_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        end_time_str = (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%dT%H:%M")

        form_data = {
            "title": "Quantum Computing 101",
            "description": "An introduction to qubits, superpositions, and algorithms.",
            "speaker": "Prof. Sharo",
            "start_time": start_time_str,
            "end_time": end_time_str,
            "location": "Room C",
            "category": "Technical",
        }

        # Submit data
        response = self.client.post("/add-event", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Event successfully created and scheduled!", response.data.decode("utf-8"))

        # Check database directly
        with app.app_context():
            db_event = Event.query.filter_by(title="Quantum Computing 101").first()
            self.assertIsNotNone(db_event)
            self.assertEqual(db_event.speaker, "Prof. Sharo")
            self.assertEqual(db_event.location, "Room C")

    def test_add_event_chronology_error(self):
        """Verify server-side rejection if the start time is equal/after end time."""
        start_time_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        # Set end time identical to start time
        end_time_str = start_time_str

        form_data = {
            "title": "Invalid Chronology Talk",
            "description": "This talk ends before it starts.",
            "speaker": "Time Traveler",
            "start_time": start_time_str,
            "end_time": end_time_str,
            "location": "Tardis",
            "category": "Keynote",
        }

        response = self.client.post("/add-event", data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error: Event start time must be before the end time.", response.data.decode("utf-8"))

    def test_add_event_missing_fields(self):
        """Verify error is thrown when form is submitted with empty fields."""
        form_data = {
            "title": "",  # Empty
            "description": "Short description.",
            "speaker": "Speaker Name",
            "start_time": "2026-06-12T09:00",
            "end_time": "2026-06-12T10:00",
            "location": "Room 5",
            "category": "Workshop",
        }

        response = self.client.post("/add-event", data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required.", response.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
