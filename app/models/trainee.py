from datetime import datetime

from app.extensions import db


class Trainee(db.Model):
    __tablename__ = "trainees"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False,
        unique=True,
        index=True
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    experience = db.Column(
        db.String(30),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    registrations = db.relationship(
        "Registration",
        back_populates="trainee",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "experience": self.experience,
            "created_at": self.created_at.isoformat()
        }