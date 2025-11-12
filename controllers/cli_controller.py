from flask import Blueprint
from init import db
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")

@db_commands.cli.command("seed")
def seed_tables():
    # Create an instance of the Model
    students = [Student(
        name="Alice",
        email="alice@email.com",
        address="Syd"
    ), Student(
        name="Bob",
        email="bob@email.com"
    )]
    # Add to the session
    db.session.add_all(students)

    teachers = [
        Teacher(
            name="Teacher 1",
            department="Science",
            address="Syd"
        ), Teacher(
            name="Teacher 2",
            department="Management",
            address="Bris"
        )
    ]
    
    # Add the teachers info to the session
    db.session.add_all(teachers)

    # Commit
    db.session.commit()

    courses = [
        Course(
            name="Physics",
            duration=3,
            teacher_id=teachers[0].teacher_id
        ),
                Course(
            name="Chemistry",
            duration=3,
            teacher_id=teachers[0].teacher_id
        ),        Course(
            name="Biology",
            duration=3,
            teacher_id=teachers[0].teacher_id
        ),        Course(
            name="Mathematics",
            duration=3,
            teacher_id=teachers[1].teacher_id
        ),        Course(
            name="Accounting",
            duration=3,
            teacher_id=teachers[1].teacher_id
        )
    ]

    # Add the courses info to the session
    db.session.add_all(courses)

    # Commit
    db.session.commit()

    enrolments = [
        Enrolment(
            enrolment_date="2025-09-28",
            student_id = students[0].student_id,
            course_id = courses[0].course_id
        ),
        Enrolment(
            enrolment_date="2025-09-28",
            student_id = students[1].student_id,
            course_id = courses[1].course_id
        ),
        Enrolment(
            enrolment_date="2025-09-28",
            student_id = students[0].student_id,
            course_id = courses[1].course_id
        )
    ]

    db.session.add_all(enrolments)

    db.session.commit()

    print("Tables seeded.")