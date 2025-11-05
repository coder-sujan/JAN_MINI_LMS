from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Teacher(db.Model):
    __tablename__ = "teachers"
     
    teacher_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(100), nullable = False, unique=True)
    address = db.Column(db.String(100))
  

#Student Schema 

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        

#object defined 
teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many = True)

    