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
    
    # print("the name of the students:", students_list.name)
    #return the jsonify(list)
    
    #imp
    if data:
        return jsonify(data)
    else:
        return {"message": "No Records Found!. Add a student to get started with system..."}
    
# GET /students/id
@students_bp.route("/<int:student_id>")
def get_students(student_id):
    #define the statement: Select * from students where id = student_id;
    stmt = db.select(Student).where(Student.student_id == student_id)
    #execture it
    student = db.session.scalar(stmt)
    #serialise it
    data = student_schema.dump(student)
    if data:
        #return it
        return jsonify(data)
    else:
        return {"message": f"Student with id: {student_id} does not exist..."}
        


# POST /students
# PUT/PATCH /students/id
# DELETE /students/id
