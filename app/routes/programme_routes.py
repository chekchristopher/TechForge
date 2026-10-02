from datetime import datetime

from flask import Blueprint, request

from app.extensions import db
from app.models import Programme


programme_bp = Blueprint(
    "programmes",
    __name__,
    url_prefix="/api/programmes"
)


@programme_bp.get("")
def get_programmes():

    query = Programme.query

    search = request.args.get("search")
    category = request.args.get("category")
    status = request.args.get("status")

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            db.or_(
                Programme.name.ilike(search_term),
                Programme.category.ilike(search_term),
                Programme.instructor.ilike(search_term)
            )
        )

    if category:
        query = query.filter(
            Programme.category == category
        )

    if status:
        query = query.filter(
            Programme.status == status
        )

    programmes = query.order_by(
        Programme.start_date.asc()
    ).all()

    return {
        "success": True,
        "count": len(programmes),
        "data": [
            programme.to_dict()
            for programme in programmes
        ]
    }


@programme_bp.get("/<int:programme_id>")
def get_programme(programme_id):

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

    return {
        "success": True,
        "data": programme.to_dict()
    }


@programme_bp.post("")
def create_programme():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "category",
        "duration",
        "price",
        "start_date",
        "instructor",
        "available_slots"
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        return {
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": "Required fields are missing.",
            "fields": missing
        }, 400

    try:

        programme = Programme(
            name=data["name"].strip(),
            category=data["category"].strip(),
            duration=data["duration"].strip(),
            price=float(data["price"]),
            start_date=datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            ).date(),
            instructor=data["instructor"].strip(),
            available_slots=int(
                data["available_slots"]
            ),
            status=data.get(
                "status",
                "upcoming"
            )
        )

        if programme.price < 0:
            raise ValueError("Price cannot be negative.")

        if programme.available_slots < 0:
            raise ValueError(
                "Available slots cannot be negative."
            )

        db.session.add(programme)
        db.session.commit()

        return {
            "success": True,
            "message": "Programme created successfully.",
            "data": programme.to_dict()
        }, 201

    except ValueError as error:

        db.session.rollback()

        return {
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": str(error)
        }, 400


@programme_bp.put("/<int:programme_id>")
def update_programme(programme_id):

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

    data = request.get_json(silent=True) or {}

    try:

        if "name" in data:
            programme.name = data["name"].strip()

        if "category" in data:
            programme.category = data["category"].strip()

        if "duration" in data:
            programme.duration = data["duration"].strip()

        if "price" in data:
            programme.price = float(data["price"])

        if "start_date" in data:
            programme.start_date = datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            ).date()

        if "instructor" in data:
            programme.instructor = data["instructor"].strip()

        if "available_slots" in data:
            new_slots = int(data["available_slots"])

            if new_slots < 0:
                raise ValueError(
                    "Available slots cannot be negative."
                )

            programme.available_slots = new_slots

        if "status" in data:
            programme.status = data["status"]

        db.session.commit()

        return {
            "success": True,
            "message": "Programme updated successfully.",
            "data": programme.to_dict()
        }

    except ValueError as error:

        db.session.rollback()

        return {
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": str(error)
        }, 400


@programme_bp.delete("/<int:programme_id>")
def delete_programme(programme_id):

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

    db.session.delete(programme)
    db.session.commit()

    return {
        "success": True,
        "message": "Programme deleted successfully."
    }