import os
import tempfile
import unittest

os.environ["SECRET_KEY"] = "test-secret"
os.environ["DATABASE_PATH"] = os.path.join(tempfile.gettempdir(), "academic_stress_manager_test.db")

from app import app
from models import db


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def register_and_login(self):
        self.client.post(
            "/register",
            data={"username": "student", "email": "student@example.com", "password": "password123"},
        )
        response = self.client.post(
            "/login",
            data={"username": "student", "password": "password123"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dashboard", response.data)

    def test_home_redirects_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_student_flow_dashboard_and_chart(self):
        self.register_and_login()
        self.client.post(
            "/assignments/add",
            data={
                "subject": "DBMS",
                "title": "Normalization Report",
                "deadline": "2099-01-03",
                "estimated_effort": "8",
                "difficulty": "4",
            },
            follow_redirects=True,
        )
        self.client.post(
            "/assignments/add",
            data={
                "subject": "AI",
                "title": "Search Algorithm Lab",
                "deadline": "2099-01-05",
                "estimated_effort": "5",
                "difficulty": "3",
            },
            follow_redirects=True,
        )
        self.client.post(
            "/exams/add",
            data={"subject": "DBMS", "exam_date": "2099-01-04"},
            follow_redirects=True,
        )

        dashboard = self.client.get("/dashboard")
        self.assertEqual(dashboard.status_code, 200)
        self.assertIn(b"Recommended order", dashboard.data)
        self.assertIn(b"Collision", dashboard.data)
        self.assertIn(b"Recommended because", dashboard.data)

        chart = self.client.get("/api/dashboard/chart")
        self.assertEqual(chart.status_code, 200)
        payload = chart.get_json()
        self.assertEqual(len(payload["labels"]), 8)
        self.assertEqual(len(payload["data"]), 8)


if __name__ == "__main__":
    unittest.main()
