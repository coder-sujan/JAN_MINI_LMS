from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow import ValidationError
from psycopg2 import errorcodes

from init import db
from models.course import Course
from schemas.schemas import course_schema, courses_schema 
# from models.course import Course, course_schema, courses_schema


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# READ - GET /
@courses_bp.route("/")
def get_courses():
    # Define the statement
    stmt = db.select(Course)
    # Execute it
    courses_list = db.session.scalars(stmt)

    # serialise it
    data = courses_schema.dump(courses_list)
    # If it exists:
    if data:
        # return it
        return jsonify(data)
    # Else:
    else:
        # Acknowledge
        return {"message": "No courses created yet."}, 404


# READ a course - GET /course_id
@courses_bp.route("/<int:course_id>")
def get_a_course(course_id):
    # Define the statement
    # SQL: SELECT * FROM courses WHERE course_id = course_id;
    stmt = db.select(Course).where(Course.course_id == course_id)
    # excute it
    course = db.session.scalar(stmt)
    # serialise it
    data = course_schema.dump(course)

    # if the course exists
    if data:
        # return it
        return jsonify(data)
    # else
    else:
        # ack
        return {"message": f"Course with id: {course_id} does not exist"}, 404

# CREATE - POST /
@courses_bp.route("/", methods=["POST"])
def create_course():
    # try:
        # Step by step methodical approach
        
        # # Get the data from the Request Body
        # body_data = request.get_json()
        # # Create a course instance
        # new_course = Course(
        #     name = body_data.get("name"),
        #     duration = body_data.get("duration"),
        #     teacher_id = body_data.get("teacher_id")
        # )
        # # Add to the session
        # db.session.add(new_course)

        ########################################        
        # schema.dump approach
        # Use the Marshmallow to validate + create the course
    #     new_course = course_schema.load(
    #         request.get_json(),
    #         session=db.session
    #     )
    #     # Add to the session
    #     db.session.add(new_course)
        
    #     # commit it
    #     db.session.commit()
    #     # Return the response
    #     return jsonify(course_schema.dump(new_course)), 201
    # except ValidationError as err:
    #     return err.messages, 400
    # except IntegrityError as err:
    #     # if int(err.orig.pgcode) == 23502: # not null violation
    #     if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
    #         return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
    #     if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
    #         return {"message": err.orig.diag.message_detail}, 409
        
    #     if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
    #         # return {"message": err.orig.diag.message_detail}, 409
    #         return {"message": "Invalid teacher selected."}, 409
    #     else:
    #         return  {"message": "Integrity Error occured."}, 409
    # except Exception as err:
    #     print(f"{err}")
    #     return {"message": "Unexpected error occured."}, 400
    
    #######################################################
    # Implementing Global Error handlers
    # Get the request body data values
    body_data = request.get_json()
    # Validate and create a course
    new_course = course_schema.load(
        body_data,
        session=db.session
    )
    # Add to the session
    db.session.add(new_course)
    # Commit it 
    db.session.commit()
    # Return the newly created course
    return course_schema.dump(new_course), 201
        
# DELETE - DELETE /course_id
@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    # Find the course to delete
    # stmt = db.select(Course).filter_by(course_id = course_id)
    # Define the stmt
    stmt = db.select(Course).where(Course.course_id == course_id)
    # Execute it
    course = db.session.scalar(stmt)
    # Serialise it
    data = course_schema.dump(course)
    # If the course exists
    if data:
        # delete
        db.session.delete(course)
        # commit
        db.session.commit()
        # Acknowledge
        return {"message": f"Course with name: {course.name} deleted successfully."}
    # Else:
    else:
        # Ack
        return {"message": f"Course with id: {course_id} cannot be found."}, 404

# UPDATE - PUT/PATCH /course_id
@courses_bp.route("/<int:course_id>", methods=["PUT", "PATCH"])
# def update_a_course(course_id):
#     try:
#         # Find the course from the db
#         stmt = db.select(Course).where(Course.course_id == course_id)
#         course = db.session.scalar(stmt)

#         data = course_schema.dump(course)
#         # if it exists:
#         if data:
#             # Get the data to update from the request body
#             body_data = request.get_json()
#             # make the changes
#             course.name = body_data.get("name") or course.name
#             course.duration = body_data.get("duration") or course.duration
#             course.teacher_id = body_data.get("teacher_id") or course.teacher_id
#             # commit
#             db.session.commit()
#             # return the response
#             return jsonify(course_schema.dump(course))
#         # else:
#         else:
#             # ack
#             return {"message": f"Course with id {course_id} does not exist."}, 404
#     except IntegrityError as err:
#         # if int(err.orig.pgcode) == 23502: # not null violation
#         if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
#             return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
#         if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
#             return {"message": err.orig.diag.message_detail}, 409
        
#         if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
#             # return {"message": err.orig.diag.message_detail}, 409
#             return {"message": "Invalid teacher selected."}, 409
#         else:
#             return  {"message": "Integrity Error occured."}, 409
#     except DataError as err:
#         return {"message": f"{err.orig.diag.message_primary}"}, 409
#     except:
#         return {"message": "Unexpected error occured."}, 400  

def update_a_course(course_id):
    # Find the course from the db
    course = db.session.get(Course, course_id)
    
    # if the course doesn't exist, return an error message
    if not course:
        return {"message": f"Course with id {course_id} does not exist."}, 404
    
    try:
        # Get the values to be updated from the request body
        body_data = request.get_json()
        # Update the values
        course = course_schema.load(
            body_data, 
            instance=course,
            session=db.session,
            partial=True
            )
        # commit
        db.session.commit()
        # return
        return course_schema.dump(course), 200
    
    except ValidationError as err:
        return err.messages, 400
    
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
            # return {"message": err.orig.diag.message_detail}, 409
            return {"message": "Invalid teacher selected."}, 409
        else:
            return  {"message": "Integrity Error occured."}, 409
    except DataError as err:
        return {"message": f"{err.orig.diag.message_primary}"}, 409
    except:
        return {"message": "Unexpected error occured."}, 400  