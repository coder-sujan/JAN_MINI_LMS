from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Course(db.Model):
    __tablename__ = "courses"
    
    
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    course_id = db.Column(db.Integer, primary_key=True)
    
    
    #foreign Key Addition / connecting teachers table here...
    teacher_id = db.Column(db.Integer, db.ForeignKey("techers.teacher_id"), nullable =False)
    
    
class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        

#object defined 
course_schema = CourseSchema()
courses_schema = CourseSchema(many = True)