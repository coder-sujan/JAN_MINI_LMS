from flask import Blueprint, jsonify, request
from init import db
from models.course import Course, course_schema, courses_schema


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# CREATE - POST /courses

# READ - GET /courses and get /course/id

@courses_bp.route("/")
def get_courses():
    #dif the statement
    stmt = db.select(Course)
    #ex it
    courses_list = db.session.scalars(stmt)
    
    
    #serialse it
    data = courses_schema.dump(courses_list)
    #if it exists:
    if data:
        
        #return it
        return jsonify(data)
        
    #else:
    else :
        #something else
        return{"message": "No Courses Created or Assigned Yet!!"}, 404


# UPDATE - PUT/PATCH /courses/id


# DELETE - DELETE /courses/id
