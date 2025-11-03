from flask import Blueprint, jsonify, request
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
def get_a_student(student_id):
    #define the statement: Select * from students where id = student_id;
    stmt = db.select(Student).where(Student.student_id == student_id)
    #execture it
    student = db.session.scalar(stmt)
    #serialise it
    data = student_schema.dump(student)
    
    # print("")
    
    if data:
        #return it
        return jsonify(data)
    else:
        return {"message": f"Student with id: {student_id} does not exist..."}
        


# POST /students
@students_bp.route("/", methods=["POST"])
def create_students():
    # get details from request body
    body_data = request.get_json()
    #create a student object with the request body data
    email = body_data.get("email")
    
    stmt = db.select(Student).where(Student.email == email)
    #adding to the session
    student = db.session.scalar(stmt)
    #checking the system with sam email add (validfation)
    data = student_schema.dump(student)
    
    #display message with same email add isuues...
    if data:
        return {"message": f"The Student with email:{email} already exists. suggestions ()"}
     
    new_student = Student(
        name = body_data.get("name"),
        email = body_data.get("email"),
        address = body_data.get("address")
    )
    #add to the session
    db.session.add(new_student)
    # Commit the session
    db.session.commit()
    #send Ack
    #creating a new variable data and stoing everything in there
    data = student_schema.dump(new_student)
    #calling that data to convert with jsonify 
    return jsonify(data), 201
#fileds cannot be empty

#Email unique error

#default errors - unexpected error occured.

#404 error occurd!
    
# PUT/PATCH /students/id
# DELETE /students/id
