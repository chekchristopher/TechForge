from datetime import datetime

from app.extensions import db


class Registration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    trainee_id = db.Column(
        db.Integer,
        db.ForeignKey("trainees.id"),
        nullable=False
    )

    programme_id = db.Column(
        db.Integer,
        db.ForeignKey("programmes.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="confirmed"
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    registered_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    trainee = db.relationship(
        "Trainee",
        back_populates="registrations"
    )

    programme = db.relationship(
        "Programme",
        back_populates="registrations"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "trainee_id",
            "programme_id",
            name="unique_trainee_programme"
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "trainee_id": self.trainee_id,
            "programme_id": self.programme_id,
            "status": self.status,
            "message": self.message,
            "registered_at": self.registered_at.isoformat(),

            "trainee": (
                self.trainee.to_dict()
                if self.trainee else None
            ),

            "programme": (
                self.programme.to_dict()
                if self.programme else None
            )
        }