"""
Main Flask Application for the Conference Event Tracker.

This module handles routing, database initialization, form submissions,
and server-side input validation for managing conference events.
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Event

app = Flask(__name__)
# Set secure random secret key for flash messaging
app.secret_key = os.environ.get("SECRET_KEY", "dev-conference-secret-key-12345")

# Configure SQLite Database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conference.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize DB with App
db.init_app(app)


def seed_sample_events():
    """Seed the database with high-quality sample conference sessions if empty."""
    if Event.query.count() == 0:
        sample_events = [
            Event(
                title="Opening Keynote: The Future of AI in Modern Engineering",
                description="An inspiring talk on how agentic systems and advanced LLMs are transforming software engineering paradigms, architecture design, and human-AI collaboration.",
                speaker="Dr. Angela Chen",
                start_time=datetime(2026, 6, 12, 9, 0),
                end_time=datetime(2026, 6, 12, 10, 30),
                location="Grand Ballroom A",
                category="Keynote",
            ),
            Event(
                title="Workshop: Architectural Patterns for High-Throughput APIs",
                description="Hands-on workshop exploring event-driven systems, caching strategies, and robust performance optimization techniques in distributed python services.",
                speaker="Marcus Vance",
                start_time=datetime(2026, 6, 12, 11, 0),
                end_time=datetime(2026, 6, 12, 13, 0),
                location="Workshop Room 102",
                category="Workshop",
            ),
            Event(
                title="Panel: Navigating Ethical Challenges in Autonomous Systems",
                description="A lively panel discussion with industry experts regarding safety guidelines, transparency, bias mitigation, and developer accountability.",
                speaker="Panel Discussion",
                start_time=datetime(2026, 6, 12, 14, 0),
                end_time=datetime(2026, 6, 12, 15, 30),
                location="Main Auditorium",
                category="Panel",
            ),
            Event(
                title="Deep Dive: Advanced CSS & Layout Techniques",
                description="Learn the secrets behind breathtaking visual design, container queries, custom subgrids, scroll-driven animations, and high-fidelity fluid typography.",
                speaker="Sofia Rodrigues",
                start_time=datetime(2026, 6, 13, 10, 0),
                end_time=datetime(2026, 6, 13, 11, 30),
                location="Hall B",
                category="Technical",
            ),
        ]
        db.session.bulk_save_objects(sample_events)
        db.session.commit()


# Create tables and seed data
with app.app_context():
    db.create_all()
    seed_sample_events()


@app.route("/")
def index():
    """
    Render the Dashboard with all events.

    Supports quick search via query parameter or returns HTML view.
    """
    events = Event.query.order_by(Event.start_time.asc()).all()
    # Unique categories to populate filtering chips dynamically
    categories = sorted(list(set(event.category for event in events)))
    return render_template("index.html", events=events, categories=categories)


@app.route("/add-event", methods=["GET", "POST"])
def add_event():
    """
    Handle event creation page and POST submission.

    Performs rigorous server-side validation.
    """
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        speaker = request.form.get("speaker", "").strip()
        start_time_str = request.form.get("start_time", "").strip()
        end_time_str = request.form.get("end_time", "").strip()
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "").strip()

        # Validate non-empty fields
        if not all([title, description, speaker, start_time_str, end_time_str, location, category]):
            flash("All fields are required. Please fill out the form completely.", "danger")
            return render_template("add_event.html"), 400

        try:
            # Parse datetime fields
            # Input format from datetime-local is typically 'YYYY-MM-DDTHH:MM'
            start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
            end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date or time format. Please use the picker.", "danger")
            return render_template("add_event.html"), 400

        # Validate schedule chronology
        if start_time >= end_time:
            flash("Error: Event start time must be before the end time.", "danger")
            return render_template("add_event.html"), 400

        # Create and commit new event
        new_event = Event(
            title=title,
            description=description,
            speaker=speaker,
            start_time=start_time,
            end_time=end_time,
            location=location,
            category=category,
        )
        try:
            db.session.add(new_event)
            db.session.commit()
            flash("Event successfully created and scheduled!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred saving the event to the database: {str(e)}", "danger")
            return render_template("add_event.html"), 500

    return render_template("add_event.html")


@app.route("/api/events")
def api_events():
    """
    API endpoint to fetch all events as JSON.

    Useful for dynamic async client side rendering or testing.
    """
    events = Event.query.order_by(Event.start_time.asc()).all()
    return jsonify([event.to_dict() for event in events])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
