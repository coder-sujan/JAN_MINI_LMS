from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp, Range, OneOf
from marshmallow import fields, ValidationError, validates

from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

#StudentSchema

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        # define the order in which the key value pair is displayed
        fields = ("student_id", "name", "email", "enrolments", "address")
    
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=("student",)))

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

#TeacherSchema

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        # define the exact order of keys
        fields = ("teacher_id", "name", "department", "courses", "address")
    
    # The valid department values: Science, Management, Engineering
    department = auto_field(validate=OneOf(
        ["Science", "Management", "Engineering"],
        error="Only valid departments are: Science, Management, Engineering"
        ))
    
    courses = fields.List(fields.Nested("CourseSchema", exclude=("teacher","teacher_id")))

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)

#CourseSchema

class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instace = True
        include_fk = True
        fields = ("course_id", "name", "duration", "teacher", "teacher_id", "enrolments")

    # name: cannot be blank, starts with letter, allows letters/numbers/spaces
    name = auto_field(validate=[
        Length(min=3, max=50, error="Course Name cannot be less than 3 or more than 50 characters in length."),
        Regexp(r"^[A-Za-z][A-Za-z0-9 ]*$", error="Name must start with a letter and must contain only letters, numbers or spaces.")
    ])
    
    # Method 1: use "validate" argument/parameter
    # duration = auto_field(validate=[
    #     Range(min=1, min_inclusive=True, error="Duration must be greater or equal to 1.")
    # ])
    
    # Method 2: use @validates decorator
    # @validates('property-to-validate')
    # def fn_name(self, property-to-validate, data_key)
    @validates('duration')
    def validates_duration(self, duration, data_key):
        if duration <= 1:
            raise ValidationError("Duration cannot be less than 1.")
    
    teacher = fields.Nested("TeacherSchema", dump_only=True, only=("name", "department"))
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=("course",)))


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


#EnrolmentSchema

class EnrolmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrolment
        load_instance = True
        include_fk = True
        fields = ("id", "enrolment_date", "student", "course")
    
    student = fields.Nested("StudentSchema", only=("student_id", "name"))
    course = fields.Nested("CourseSchema", only=("course_id", "name", "duration"))

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many=True)