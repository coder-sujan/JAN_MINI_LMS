from flask import Blueprint, jsonify, request
from init import db
from models.course import Course, course_schema, courses_schema


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

