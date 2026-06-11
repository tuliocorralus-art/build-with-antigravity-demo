# OmniEvent - Conference Event Tracker

OmniEvent is a sleek, premium, dark-themed web application designed to help conference attendees, speakers, and organizers effortlessly track scheduled events, sessions, and workshops, discover upcoming talks, and schedule new sessions dynamically.

---

## ✨ Features

- **Dynamic Glassmorphic Dashboard:** Immersive, high-performance UI styled with custom CSS glassmorphic tokens, deep HSL colors, neon accents, and smooth hover micro-animations.
- **Real-Time Client-Side Search:** Instant card filtering as you type, matching titles, speakers, descriptions, and locations.
- **Track Classification Chips:** Categorize and dynamically filter events instantly by session type (Keynote, Workshop, Technical Talk, Panel Discussion, etc.).
- **Automatic Seed Seeding:** Database automatically seeds itself with realistic, premium sessions on first launch so the platform never looks empty.
- **Robust DateTime Validations:** Prevents chronological scheduling errors (e.g., sessions ending before they start) with active validation feedback on both client-side and server-side forms.
- **Animated Flash Notifications:** Toast banners slide in dynamically to confirm scheduling events, auto-dimming and self-removing after 5 seconds.

---

## 🛠️ Tech Stack

- **Backend:** Python 3 (Flask, Flask-SQLAlchemy)
- **Frontend:** Responsive HTML5, Vanilla CSS3 (Custom Glassmorphism, Google Fonts: Outfit & Inter, CSS Transitions), Vanilla JS (ES6)
- **Database:** SQLite3 (Local embedded relational file)
- **Virtualization:** Clean Python Isolation (`venv`)

---

## 📂 Project Structure

```
conference_tracker/
├── app.py                  # Main Flask application entrypoint
├── models.py               # SQLAlchemy schema definition for Event
├── requirements.txt        # Isolated Python environment dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Premium custom stylesheet
│   └── js/
│       └── main.js         # Client-side filtering and notification logic
├── templates/
│   ├── base.html           # Universal structure, Google fonts & Toast container
│   ├── index.html          # Interactive event-grid dashboard
│   └── add_event.html      # Glassmorphic form submission view
└── tests/
    ├── test_app.py         # Route & validation integration tests
    └── test_models.py      # Event model unit tests
```

---

## 🚀 Quickstart Guide

### 1. Prerequisite Environment Setup
Navigate to the directory and initialize an isolated Python virtual environment:
```bash
cd conference_tracker/
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
Install all package dependencies securely from PyPI:
```bash
pip install -r requirements.txt
```

### 3. Launch the Server
Execute the Flask server:
```bash
python3 app.py
```
The server will bind locally. Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

---

## 🧪 Running the Test Suite

We've designed a thorough, custom test suite with complete code coverage for backend logic:

Configure Python path and run the standard discovery engine:
```bash
export PYTHONPATH=.
python3 -m unittest discover -s tests
```

#### Verified Test Scenarios:
- DB initialization and mock data automatic-seeding.
- Home template rendering, card population, and search indexes.
- REST API `/api/events` serialization.
- Form inputs, validation boundaries, and redirect responses.
- Chronology controls (rejects start time >= end time).
- Event serialization dictionary mappings (`to_dict`) and representation outputs (`__repr__`).
