from flask import Blueprint, jsonify
from init import db
from models.student import Student, student_schema, students_schema


students_bp = Blueprint("students", __name__, url_prefix="/students")



# Our Routesto be defined....

# GET /students

@students_bp.route("/")
def get_students():
    #first define a statement: Select * from students;
    stmt = db.select(Student)
    #execute it
    students_list = db.session.scalars(stmt)
    #serialise it
    data = students_schema.dump(students_list)
    #return the jsonify(list)
    if data:
        return jsonify(data)
    else:
        return {"message": "No Records Found!. Add a student to get started with system..."}
    
# GET /students/id
# POST /students
# PUT/PATCH /students/id
# DELETE /students/id
