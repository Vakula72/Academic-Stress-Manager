# AI-Assisted Assignment Collision Detector & Academic Stress Manager

A Flask + SQLite web app for college students to manage assignments and exams, detect deadline collisions, analyze stressful weeks, and get explainable priority recommendations.

## Features

- Student registration, login, logout, and password hashing
- Student-specific assignment and exam records
- Assignment CRUD plus completion tracking with actual time spent
- Exam CRUD
- Deadline collision alerts for same-week assignment overload and assignments near exams
- Weekly stress classification: Normal, Busy, High Stress
- Explainable priority recommendations using urgency, difficulty, and effort
- Chart.js workload visualization

## Local Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000`.

## Environment Variables

- `SECRET_KEY`: set this in production for secure sessions.
- `PORT`: optional local port override. Defaults to `5000`.
- `FLASK_DEBUG=1`: enables debug mode locally.
- `DATABASE_PATH`: optional SQLite file path. Defaults to `database.db` in the project folder.
- `DATABASE_URL`: optional full SQLAlchemy database URL. If set, it takes priority over `DATABASE_PATH`.

## Deploy

This project includes a `Procfile` and `wsgi.py`, so Python hosts that support Procfile-based apps can start it with:
