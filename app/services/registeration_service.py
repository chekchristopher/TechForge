from app.extensions import db
from app.models import (
    Programme,
    Trainee,
    Registration
)


def register_trainee(data):

    programme_id = data.get("programme_id")

    if not programme_id:
        return {
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": "programme_id is required."
        }, 400

    programme = db.session.get(
        Programme,
        programme_id
    )

    if not programme:

        return {
            "success": False,
            "error": "PROGRAMME_NOT_FOUND",
            "message": "Programme not found."
        }, 404


    # Programme must accept registrations.
    if programme.status != "open":

        return {
            "success": False,
            "error": "PROGRAMME_NOT_OPEN",
            "message": (
                "This programme is not currently "
                "accepting registrations."
            )
        }, 409


    # Slot exhaustion rule.
    if programme.available_slots <= 0:

        return {
            "success": False,
            "error": "SLOT_EXHAUSTED",
            "message": (
                "This programme has no available slots."
            )
        }, 409


    email = data.get(
        "email",
        ""
    ).strip().lower()


    if not email:

        return {
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": "Email is required."
        }, 400


    trainee = Trainee.query.filter_by(
        email=email
    ).first()


    if not trainee:

        trainee = Trainee(
            full_name=data.get(
                "full_name",
                ""
            ).strip(),

            email=email,

            phone=data.get(
                "phone",
                ""
            ).strip(),

            experience=data.get(
                "experience",
                ""
            ).strip()
        )

        db.session.add(trainee)
        db.session.flush()


    # Prevent duplicate registration.
    existing_registration = Registration.query.filter_by(
        trainee_id=trainee.id,
        programme_id=programme.id
    ).first()


    if existing_registration:

        return {
            "success": False,
            "error": "ALREADY_REGISTERED",
            "message": (
                "This trainee is already registered "
                "for this programme."
            )
        }, 409


    # Create registration.
    registration = Registration(
        trainee_id=trainee.id,
        programme_id=programme.id,
        status="confirmed",
        message=data.get("message")
    )


    # Decrease available slot.
    programme.available_slots -= 1


    # Automatically close programme when final slot is taken.
    if programme.available_slots == 0:
        programme.status = "closed"


    db.session.add(registration)
    db.session.commit()


    return {
        "success": True,
        "message": "Registration completed successfully.",
        "data": registration.to_dict()
    }, 201