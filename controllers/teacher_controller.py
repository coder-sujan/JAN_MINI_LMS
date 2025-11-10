from flask import Blueprint, jsonify, request
from init import db
from models.teacher import Teacher, teacher_schema, teachers_schema

from sqlalchemy.exc import IntegrityError

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")


# CREATE - POST /teachers

# READ - GET /teachers and get /teacher/id


# UPDATE - PUT/PATCH /teachers/id


# DELETE - DELETE /teachers/id



# READ - GET /teachers and get /teacher/id

@teachers_bp.route("/")
def get_teachers():
    
    #Get the department name from URL 
    department = request.args.get("department")
    
    if department:
        #define the statement for Get All teachers: Select * From teachers Where department = 'something/sci/maths';
        stmt = db.select(Teacher).where(Teacher.department == department).order_by(Teacher.teacher_id) 
    else:
        stmt = db.select(Teacher).order_by(Teacher.teacher_id)
    
    #define the stmt for GET ALL teacher: Select * From Teachers;
    # stmt = db.select(Teacher)
    #execute it
    teachers_list = db.session.scalars(stmt)
    #serialise it
    data = teachers_schema.dump(teachers_list)
    
    if data:
        #return the jsonify(list of teachers)
        return jsonify(data)
    else:
        return {"message": "No records found... Please Add or Seed a teacher to get the data.."}, 404
    

#get teacher by id
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
        
        
        

# POST /teachers
@teachers_bp.route("/", methods=["POST"])
def create_teachers():
    # get details from request body
    body_data = request.get_json()
    #create a teacher object with the request body data
    # email = body_data.get("email")
    
    
    # ERROR
    # stmt = db.select(Student).where(Student.email == email)
    #define statemnet
    #stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    
    #adding to the session
    #teacher = db.session.scalar(stmt)
    #checking the system with sam email add (validfation)
    #data = teacher_schema.dump(teacher)
    
    #display message with same email add isuues...
    # if data:
    #     return {"message": f"The Teacher with email:{email} already exists. suggestions ()"}
     
    # new_teacher = Teacher(
    #     name = body_data.get("name"),
    #     department = body_data.get("department"),
    #     address = body_data.get("address")
    # )
    
    new_teacher = teacher_schema.load(
        body_data,
        session=db.session
    )
    
    #add to the session
    db.session.add(new_teacher)
    # Commit the session
    db.session.commit()
    #send Ack
    #creating a new variable data and stoing everything in there
    data = teacher_schema.dump(new_teacher)
    #calling that data to convert with jsonify 
    return jsonify(data), 201
#fileds cannot be empty

#Email unique error

#default errors - unexpected error occured.

#404 error occurd!



# DELETE /teachers/id
@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    #find the std with id. : Select * from teacher where teacher_id = teacher_id
    stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    teacher = db.session.scalar(stmt)
    #if std exists:
    if teacher:
        
       #detele
       name = teacher.name
       db.session.delete(teacher)
       #commit
       db.session.commit()
       #return ack
       return {"message": f"Teacher with name {teacher.name} deleted successfully"}, 200
    else:
       #retun ack
       return {"message": f"Teacher with id: {teacher} does not exixt..."}, 404
    
    #else
       # return ack
       
       

# PUT/PATCH /teachers/id (EDIT the std details) updating the teacher

@teachers_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    #Get the std from db first
    try:
        #define statemnet
        stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
        #exc the stmt
        teacher = db.session.scalar(stmt)
        
        #if the std exists
        if teacher:
            #fetch the info from the request body
            body_data = request.get_json()
            # make the changes (using a short circuit method) using both put and patch
            # where put updates everything 
            # patch updates specific key values
            teacher.name = body_data.get("name", teacher.name)
            teacher.department = body_data.get("department", teacher.department)
            teacher.address = body_data.get("address", teacher.address)
            
            #commit to the db
            db.session.commit()
            # ack
            return jsonify(teacher_schema.dump(teacher))
        #else
        else:
            return {"message": f"Teacher with id: {teacher_id} does not exist"}, 404
            # ack 
    except IntegrityError as err:
        return {"Email address is already in Use "}, 409
       