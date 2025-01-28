from flask import Flask, Blueprint, jsonify, request
from models import db, User, Course, Department, AttendanceLog, Student
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from utils import log_info, log_error

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = ''
jwt = JWTManager(app)
api_bp = Blueprint('api', __name__)


def create_first_user():
    """Create the first admin user if no users exist."""
    try: 
        log_info("create_first_user function initialized")
        if not User.query.first():
            username = 'amit'
            password = 'amit@123'
            hashed_password = generate_password_hash(password)
            first_user = User(
                type="admin",
                full_name="Amit Kumar",
                username=username,
                email="amit@example.com",
                password=hashed_password,
                submitted_by="system",
                updated_by="system"
            )
            db.session.add(first_user)
            db.session.commit()
            log_info(f"First user created with username: {username} and password: {password}")
    except Exception as e:
        log_error(f"Error during first user creation: {str(e)}")
        raise e


@api_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user in the system. 
    This endpoint accepts a POST request with user details, 
    hashes the password, and stores the user information in the database.

    Returns:
        JSON response with a success message or error details.
    """
    try:
        log_info("Register function initialized")
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            type=data['type'],
            full_name=data['full_name'],
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            submitted_by=data['submitted_by']
        )
        db.session.add(new_user)
        db.session.commit()
        log_info(f"User {data['username']} created.")
        return jsonify({"message": "User created successfully!"}), 201

    except Exception as e:
        log_error(f"Error during user registration: {str(e)}")
        raise e


@api_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login. 
    This endpoint accepts a POST request with login credentials (username and password),
    validates the user's credentials, and returns an access token if the login is successful.

    Returns:
        JSON response with the access token if the login is successful, 
        or an error message if the credentials are invalid.
    """
    try:
        log_info("login function initialized")
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            log_info(f"User {data['username']} logged in.")
            return jsonify(access_token=access_token), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        log_error(f"Error during user login: {str(e)}")
        raise e

@api_bp.route('/attendance_log', methods=['GET'])
@jwt_required()
def get_all_attendance_logs():
    """
    Fetch all attendance logs. Requires JWT authentication.

    Returns:
        JSON response with a list of attendance logs.
    """
    try:
        log_info("get_all_attendance_logs function initialized")
        attendance_logs = AttendanceLog.query.all()
        result = [{"id": log.id, "student_id": log.student_id, "course_id": log.course_id,
                   "present": log.present, "submitted_by": log.submitted_by, "updated_by": log.updated_by} 
                  for log in attendance_logs]
        return jsonify(result), 200
    except Exception as e:
        log_error(f"Error fetching attendance logs: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/attendance_log', methods=['POST'])
@jwt_required()
def create_attendance_log():
    """
    Create a new attendance log entry. Requires JWT authentication.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        log_info("create_attendance_log function initialized")
        data = request.get_json()
        new_log = AttendanceLog(
            student_id=data['student_id'],
            course_id=data['course_id'],
            present=data['present'],
            submitted_by=data['submitted_by'],
            updated_by=data['updated_by']
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Attendance log created!"}), 201
    except Exception as e:
        log_error(f"Error creating attendance log: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_all_courses():
    """
    Fetch all courses. Requires JWT authentication.

    Returns:
        JSON response with a list of courses.
    """
    try:
        log_info("get_all_courses function initialized")
        courses = Course.query.all()
        result = [{"id": course.id, "course_name": course.course_name, "department_id": course.department_id,
                   "semester": course.semester, "class": course.class_name, "lecture_hours": course.lecture_hours,
                   "submitted_by": course.submitted_by, "updated_at": course.updated_at} 
                  for course in courses]
        return jsonify(result), 200
    except Exception as e:
        log_error(f"Error fetching courses: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    """
    Create a new course. Requires JWT authentication.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        log_info("create_course function initialized")
        data = request.get_json()
        new_course = Course(
            course_name=data['course_name'],
            department_id=data['department_id'],
            semester=data['semester'],
            class_name=data['class'],
            lecture_hours=data['lecture_hours'],
            submitted_by=data['submitted_by'],
            updated_at=data['updated_at']
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Course created!"}), 201
    except Exception as e:
        log_error(f"Error creating course: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """
    Fetch all users. Requires JWT authentication.

    Returns:
        JSON response with a list of users.
    """
    try:
        log_info("get_all_users function initialized")
        users = User.query.all()
        result = [{"id": user.id, "type": user.type, "full_name": user.full_name, "username": user.username,
                   "email": user.email, "submitted_by": user.submitted_by, "updated_by": user.updated_by}
                  for user in users]
        return jsonify(result), 200
    except Exception as e:
        log_error(f"Error fetching users: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """
    Create a new user. Requires JWT authentication.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        log_info("create_user function initialized")
        data = request.get_json()
        new_user = User(
            type=data['type'],
            full_name=data['full_name'],
            username=data['username'],
            email=data['email'],
            password=data['password'],
            submitted_by=data['submitted_by'],
            updated_by=data['updated_by']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created!"}), 201
    except Exception as e:
        log_error(f"Error creating user: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_all_departments():
    """
    Fetch all departments. Requires JWT authentication.

    Returns:
        JSON response with a list of departments.
    """
    try:
        log_info("get_all_departments function initialized")
        departments = Department.query.all()
        result = [{"id": dept.id, "department_name": dept.department_name,
                   "submitted_by": dept.submitted_by, "updated_at": dept.updated_at} 
                  for dept in departments]
        return jsonify(result), 200
    except Exception as e:
        log_error(f"Error fetching departments: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/departments', methods=['POST'])
@jwt_required()
def create_department():
    """
    Create a new department. Requires JWT authentication.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        log_info("create_department function initialized")
        data = request.get_json()
        new_department = Department(
            department_name=data['department_name'],
            submitted_by=data['submitted_by'],
            updated_at=data['updated_at']
        )
        db.session.add(new_department)
        db.session.commit()
        return jsonify({"message": "Department created!"}), 201
    except Exception as e:
        log_error(f"Error creating department: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/students', methods=['GET'])
@jwt_required()
def get_all_students():
    """
    Fetch all students. Requires JWT authentication.

    Returns:
        JSON response with a list of students.
    """
    try:
        log_info("get_all_students function initialized")
        students = Student.query.all()
        result = [{"id": student.id, "full_name": student.full_name, "department_id": student.department_id,
                   "class": student.class_name, "submitted_by": student.submitted_by, "updated_at": student.updated_at}
                  for student in students]
        return jsonify(result), 200
    except Exception as e:
        log_error(f"Error fetching students: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    """
    Create a new student. Requires JWT authentication.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        log_info("create_student function initialized")
        data = request.get_json()
        new_student = Student(
            full_name=data['full_name'],
            department_id=data['department_id'],
            class_name=data['class'],
            submitted_by=data['submitted_by'],
            updated_at=data['updated_at']
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student created!"}), 201
    except Exception as e:
        log_error(f"Error creating student: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
