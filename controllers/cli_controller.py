from flask import Blueprint
from init import db
from models.student import Student
from models.teacher import Teacher

db_commands = Blueprint("db", __name__) 


#CLI commands
#Create

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables Created!!")
    
    
#drop
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables Dropped!!")


#seed
@db_commands.cli.command("seed")
def seed_tables():
    
    #create an instance of the Model first
    students = [Student(
        name="Bob",
        email="bob@gmail.com",
        address ="Syd"
        ), Student(
        name="Jack",
        email="jack@gmail.com",
        )]
    
    #adding to the session
    db.session.add_all(students)
    
    
    teachers = [Teacher(
        name="Teacher 1",
        department="IT",
        address ="Mel"
        ), Teacher(
        name="Teacher 2",
        department="Science",
        address ="SYD"
        )]
    
    
    #Add the teachers into to the session
    db.session.add_all(teachers)
    
    
    #commit
    db.session.commit() 
    print("Table Seeded!") 
    
    
#select
# @db_commands.cli.command("selectall")
# def select_all():




    
    