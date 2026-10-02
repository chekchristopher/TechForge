from datetime import date

from app import create_app
from app.extensions import db
from app.models import Programme


app = create_app()


programmes = [
    Programme(
        name="Full-Stack Web Engineering",
        category="Software Development",
        duration="12 Weeks",
        price=185000,
        start_date=date(2026, 11, 9),
        instructor="Daniel Okafor",
        available_slots=18,
        status="open"
    ),

    Programme(
        name="Cybersecurity & SOC Operations",
        category="Cybersecurity",
        duration="10 Weeks",
        price=220000,
        start_date=date(2026, 11, 16),
        instructor="Amaka Nwosu",
        available_slots=12,
        status="open"
    ),

    Programme(
        name="Data Analytics with Python",
        category="Data & AI",
        duration="8 Weeks",
        price=150000,
        start_date=date(2026, 12, 1),
        instructor="Michael Adeyemi",
        available_slots=24,
        status="upcoming"
    ),

    Programme(
        name="Cloud Engineering",
        category="Cloud & DevOps",
        duration="10 Weeks",
        price=210000,
        start_date=date(2026, 11, 23),
        instructor="David Eze",
        available_slots=8,
        status="open"
    ),

    Programme(
        name="UI/UX Product Design",
        category="Design",
        duration="6 Weeks",
        price=120000,
        start_date=date(2026, 12, 7),
        instructor="Sarah Williams",
        available_slots=20,
        status="upcoming"
    )
]


with app.app_context():

    db.drop_all()
    db.create_all()

    db.session.add_all(programmes)
    db.session.commit()

    print("Database seeded successfully.")