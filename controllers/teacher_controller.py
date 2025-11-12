from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow import ValidationError

from init import db
from models.teacher import Teacher
# from schemas.schemas import teacher_schema, teachers_schema (can create seperate folder and add all the schemas)
from models.teacher import Teacher, teacher_schema, teachers_schema


teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

# CREATE - POST /
# READ - GET / AND GET /id
# UPDATE - PUT/PATCH /id
# DELETE - DELETE /id

# READ - GET /
@teachers_bp.route("/")
def get_teachers():
    # Get the department name from the URL
    department = request.args.get("department")

    if department:
        # Define the statement for GET All teacher: SELECT * FROM teachers WHERE department='something';
        stmt = db.select(Teacher).where(Teacher.department == department).order_by(Teacher.teacher_id)
    else:
        # Define the statement for GET All teacher: SELECT * FROM teachers
        stmt = db.select(Teacher).order_by(Teacher.teacher_id)
    # Execute it
    teachers_list = db.session.scalars(stmt)

    # Serialise it
    data = teachers_schema.dump(teachers_list)

    if data:
        # Return the jsonify(list)
        return jsonify(data)
    else:
        return {"message": "No records found. Add a teacher to get started."}, 404
    
# READ - GET /teacher_id
@teachers_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    # Define the statement: SELECT * FROM teachers WHERE id = teacher_id;
    stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    # Execute it
    teacher = db.session.scalar(stmt)
    # Serialise it
    data = teacher_schema.dump(teacher)
    if data:
        # Return it
        return jsonify(data)
    else:
        return {"message": f"Teacher with id: {teacher_id} does not exist."}, 404
    

# POST /
@teachers_bp.route("/", methods=["POST"])
def create_teacher():
    try:
        # GET details from the REQUEST Body
        body_data = request.get_json()
        # Create a Teacher Object with the REQUEST Body data

        # Method 1: Error handling for unique department constraint
        # department = body_data.get("department")

        # stmt = db.select(Teacher).where(Teacher.department == department)
        # teacher = db.session.scalar(stmt)
        # data = teacher_schema.dump(teacher)

        # if data:
        #     return {"message": f"The Teacher with department:{department} already exists."}, 409
        
        # new_teacher = Teacher(
        #     name = body_data.get("name"),
        #     department = body_data.get("department"),
        #     address = body_data.get("address")
        # )
        
        # schema.load() method to create the new teacher with validation rules implemented
        new_teacher = teacher_schema.load(
            body_data,
            session=db.session
        )
        
        # Add to the session
        db.session.add(new_teacher)
        # Commit the session
        db.session.commit()
        # Send ack
        data = teacher_schema.dump(new_teacher)
        return jsonify(data), 201
    
    except ValidationError as err:
        return err.messages, 400
    
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        else:
            return  {"message": "Integrity Error occured."}, 409
    except:
        return {"message": "Unexpected error occured."}
    
# DELETE /id
@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    # Find the teacher with id: SELECT * FROM teacher WHERE teacher_id=teacher_id
    stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    teacher = db.session.scalar(stmt)
    # if teacher exists:
    if teacher:
        # delete
        # name = teacher.name
        db.session.delete(teacher)
        # commit
        db.session.commit()
        # return ack
        return {"message": f"Teacher {teacher.name} deleted successfully."}
    # else
    else:
        # return ack
        return {"message": f"Teacher with id: {teacher_id} does not exist."}, 404
    
# PUT/PATCH /id
@teachers_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    # Method 1: In this method, we work on the update feature in a step-by-step approach (thorough)
    # try:
    #     # Get the teacher from the database
    #     # Define the stmt
    #     stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    #     # Execute the statement
    #     teacher = db.session.scalar(stmt)
    #     # if the teacher exists
    #     if teacher:
    #         # fetch the info from the request body
    #         body_data = request.get_json()
    #         # make the changes, short circuit method
    #         teacher.name = body_data.get("name",teacher.name)
    #         teacher.department = body_data.get("department",teacher.department)
    #         teacher.address = body_data.get("address", teacher.address)
    #         # commit to the db
    #         db.session.commit()
    
    # Method 2: Here, we are implementing the schema.load() feature for some automation
    # Get the teacher to update
    teacher = db.session.get(Teacher, teacher_id)
    # If the teacher does not exist:
    if not teacher:
        # Send an error message
        return {"message": f"The teacher with id: {teacher_id} does not exist."}, 404
    
    # try:
    try:
        # getting the body data
        body_data = request.get_json()
        # Validate and Update the values
        teacher = teacher_schema.load(
            body_data,
            instance=teacher,
            session=db.session,
            partial=True
        )
        # commit 
        db.session.commit()
        # ack   
        return jsonify(teacher_schema.dump(teacher))
        # else
    
    except ValidationError as err:
        return err.messages, 400
    
    except IntegrityError as err:
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
                return {"message": err.orig.diag.message_detail}, 409