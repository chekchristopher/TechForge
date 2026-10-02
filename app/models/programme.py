from datetime import date, datetime

from app.extensions import db


class Programme(db.Model):
    __tablename__ = "programmes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    duration = db.Column(
        db.String(50),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    instructor = db.Column(
        db.String(120),
        nullable=False
    )

    available_slots = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="upcoming"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    registrations = db.relationship(
        "Registration",
        back_populates="programme",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "duration": self.duration,
            "price": self.price,
            "start_date": self.start_date.isoformat(),
            "instructor": self.instructor,
            "available_slots": self.available_slots,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }