from flask import Blueprint, jsonify, request
from init import db
from models.teacher import Teacher, teacher_schema, teachers_schema


teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")



# CREATE - POST /teachers

# READ - GET /teachers and get /teacher/id


# UPDATE - PUT/PATCH /teachers/id


# DELETE - DELETE /teachers/id



# READ - GET /teachers and get /teacher/id

@teachers_bp.route("/")
def get_teachers():
    #define the stmt for GET ALL teacher: Select * From Teachers;
    stmt = db.select(Teacher)
    #execute it
    teachers_list = db.session.scalars(stmt)
    #serialise it
    data = teachers_schema.dump(teachers_list)
    
    if data:
        #return the jsonify(list of teachers)
        return jsonify(data)
    else:
        return {"message": "No records found... Please Add or Seed a teacher to get the data.."}, 404
    


@teachers_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    #define the statement: Select * from teachers where id = teacher_id;
    stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    #execture it
    teacher = db.session.scalar(stmt)
    #serialise it
    data = teacher_schema.dump(teacher)
    
    # print("")
    
    if data:
        #return it
        return jsonify(data)
    else:
        return {"message": f"Teacher with id: {teacher_id} does not exist..."}
        