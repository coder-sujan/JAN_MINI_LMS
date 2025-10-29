from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Student(db.Model):
    __tablename__ = "students"
     
    student_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    address = db.Column(db.String(100))
  

#Student Schema 

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        

#object defined 
student_schema = StudentSchema()
students_schema = StudentSchema(many = True)

    