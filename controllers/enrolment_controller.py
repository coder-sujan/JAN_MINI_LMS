from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")

# Read all
@enrolments_bp.route("/")
def get_enrolments():
    # Get potential filters from query params
    enrolment_id = request.args.get("enrolment_id", type=int)
    student_id = request.args.get("student_id", type=int)
    
    # define the stmt
    stmt = db.select(Enrolment)
    
    # Testing
    # print(Enrolment.enrolment.name)
    
    # Add filters based on the params provided
    if enrolment_id:
        stmt = stmt.where(Enrolment.enrolment_id == enrolment_id)
    if student_id:
        stmt = stmt.where(Enrolment.student_id == student_id)
        # stmt = stmt.filter_by(student_id = student_id)
    # execute it
    enrolments_list = db.session.scalars(stmt)
    # serliase it
    data = enrolments_schema.dump(enrolments_list)
    
    # print(data)
    if data:
        return jsonify(data)
    # return it
    else:
        return {"message": "No enrolments found."}, 404
    
# CREATE - POST /
@enrolments_bp.route("/", methods=["POST"])
def create_enrolment():
    try:
        # Get the data from the Request Body
        body_data = request.get_json()
        # Create a enrolment instance
        new_enrolment = Enrolment(
            enrolment_id = body_data.get("enrolment_id"),
            student_id = body_data.get("student_id"),
            enrolment_date = body_data.get("enrolment_date")
        )
        # Add to the session
        db.session.add(new_enrolment)
        # Commit it
        db.session.commit()
        # Return the response
        return jsonify(enrolment_schema.dump(new_enrolment)), 201
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
            # return {"message": err.orig.diag.message_detail}, 409
            return {"message": err.orig.diag.message_detail}, 409
        else:
            return  {"message": "Integrity Error occured."}, 409
    except:
        return {"message": "Unexpected error occured."}, 400
    
# DELETE - DELETE /enrolment_id
@enrolments_bp.route("/<int:enrolment_id>", methods=["DELETE"])
def delete_enrolment(enrolment_id):
    # Find the enrolment to delete
    # stmt = db.select(Enrolment).filter_by(enrolment_id = enrolment_id)
    # Define the stmt
    stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)
    # Execute it
    enrolment = db.session.scalar(stmt)
    # Serialise it
    data = enrolment_schema.dump(enrolment)
    # If the enrolment exists
    if data:
        # delete
        db.session.delete(enrolment)
        # commit
        db.session.commit()
        # Acknowledge
        return {"message": f"Enrolment with id: {enrolment_id} deleted successfully."}
    # Else:
    else:
        # Ack
        return {"message": f"Enrolment with id: {enrolment_id} cannot be found."}, 404

# UPDATE - PUT/PATCH /enrolment_id
@enrolments_bp.route("/<int:enrolment_id>", methods=["PUT", "PATCH"])
def update_an_enrolment(enrolment_id):
    try:
        # Find the enrolment from the db
        stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)
        enrolment = db.session.scalar(stmt)

        data = enrolment_schema.dump(enrolment)
        # if it exists:
        if data:
            # Get the data to update from the request body
            body_data = request.get_json()
            # make the changes
            enrolment.student_id = body_data.get("student_id") or enrolment.student_id
            enrolment.course_id = body_data.get("course_id") or enrolment.course_id
            enrolment.enrolment_date = body_data.get("enrolment_date") or enrolment.enrolment_date
            # commit
            db.session.commit()
            # return the response
            return jsonify(enrolment_schema.dump(enrolment))
        # else:
        else:
            # ack
            return {"message": f"Enrolment with id {enrolment_id} does not exist."}, 404
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
            # return {"message": err.orig.diag.message_detail}, 409
            return {"message": f"{err.orig.diag.message_primary}"}, 409
        else:
            return  {"message": "Integrity Error occured."}, 409
    except DataError as err:
        return {"message": f"{err.orig.diag.message_primary}"}, 409
    except:
        return {"message": "Unexpected error occured."}, 400  