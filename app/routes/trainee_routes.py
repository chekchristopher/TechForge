from flask import Blueprint, request

from app.extensions import db
from app.models import Trainee


trainee_bp = Blueprint(
    "trainees",
    __name__,
    url_prefix="/api/trainees"
)


@trainee_bp.get("")
def get_trainees():

    trainees = Trainee.query.order_by(
        Trainee.created_at.desc()
    ).all()

    return {
        "success": True,
        "count": len(trainees),
        "data": [
            trainee.to_dict()
            for trainee in trainees
        ]
    }


@trainee_bp.get("/<int:trainee_id>")
def get_trainee(trainee_id):

    trainee = db.session.get(
        Trainee,
        trainee_id
    )

    if not trainee:
        return {
            "success": False,
            "error": "TRAINEE_NOT_FOUND",
            "message": "Trainee not found."
        }, 404

    return {
        "success": True,
        "data": trainee.to_dict()
    }


@trainee_bp.post("")
def create_trainee():

    data = request.get_json(silent=True) or {}

    required = [
        "full_name",
        "email",
        "phone",
        "experience"
    ]

    missing = [
        field
        for field in required
        if not data.get(field)
    ]

    if missing:
        return {
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": "Required fields are missing.",
            "fields": missing
        }, 400

    email = data["email"].strip().lower()

    existing = Trainee.query.filter_by(
        email=email
    ).first()

    if existing:
        return {
            "success": False,
            "error": "EMAIL_ALREADY_EXISTS",
            "message": "A trainee with this email already exists."
        }, 409

    trainee = Trainee(
        full_name=data["full_name"].strip(),
        email=email,
        phone=data["phone"].strip(),
        experience=data["experience"].strip()
    )

    db.session.add(trainee)
    db.session.commit()

    return {
        "success": True,
        "message": "Trainee created successfully.",
        "data": trainee.to_dict()
    }, 201


@trainee_bp.put("/<int:trainee_id>")
def update_trainee(trainee_id):

    trainee = db.session.get(
        Trainee,
        trainee_id
    )

    if not trainee:
        return {
            "success": False,
            "error": "TRAINEE_NOT_FOUND",
            "message": "Trainee not found."
        }, 404

    data = request.get_json(silent=True) or {}

    if "full_name" in data:
        trainee.full_name = data["full_name"].strip()

    if "email" in data:
        email = data["email"].strip().lower()

        duplicate = Trainee.query.filter(
            Trainee.email == email,
            Trainee.id != trainee.id
        ).first()

        if duplicate:
            return {
                "success": False,
                "error": "EMAIL_ALREADY_EXISTS",
                "message": "Email already belongs to another trainee."
            }, 409

        trainee.email = email

    if "phone" in data:
        trainee.phone = data["phone"].strip()

    if "experience" in data:
        trainee.experience = data["experience"].strip()

    db.session.commit()

    return {
        "success": True,
        "message": "Trainee updated successfully.",
        "data": trainee.to_dict()
    }


@trainee_bp.delete("/<int:trainee_id>")
def delete_trainee(trainee_id):

    trainee = db.session.get(
        Trainee,
        trainee_id
    )

    if not trainee:
        return {
            "success": False,
            "error": "TRAINEE_NOT_FOUND",
            "message": "Trainee not found."
        }, 404

    db.session.delete(trainee)
    db.session.commit()

    return {
        "success": True,
        "message": "Trainee deleted successfully."
    }