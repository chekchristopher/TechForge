from flask import Blueprint, request

from app.extensions import db
from app.models import Registration

from app.services.registration_service import (
    register_trainee
)


registration_bp = Blueprint(
    "registrations",
    __name__,
    url_prefix="/api/registrations"
)


@registration_bp.get("")
def get_registrations():

    registrations = Registration.query.order_by(
        Registration.registered_at.desc()
    ).all()

    return {
        "success": True,
        "count": len(registrations),
        "data": [
            registration.to_dict()
            for registration in registrations
        ]
    }


@registration_bp.get("/<int:registration_id>")
def get_registration(registration_id):

    registration = db.session.get(
        Registration,
        registration_id
    )

    if not registration:

        return {
            "success": False,
            "error": "REGISTRATION_NOT_FOUND",
            "message": "Registration not found."
        }, 404

    return {
        "success": True,
        "data": registration.to_dict()
    }


@registration_bp.post("")
def create_registration():

    data = request.get_json(
        silent=True
    ) or {}

    required = [
        "programme_id",
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

    return register_trainee(data)


@registration_bp.delete(
    "/<int:registration_id>"
)
def cancel_registration(registration_id):

    registration = db.session.get(
        Registration,
        registration_id
    )

    if not registration:

        return {
            "success": False,
            "error": "REGISTRATION_NOT_FOUND",
            "message": "Registration not found."
        }, 404


    programme = registration.programme

    db.session.delete(registration)


    # Return the slot when a registration is cancelled.
    if programme:

        programme.available_slots += 1

        if programme.status == "closed":
            programme.status = "open"


    db.session.commit()


    return {
        "success": True,
        "message": "Registration cancelled successfully."
    }