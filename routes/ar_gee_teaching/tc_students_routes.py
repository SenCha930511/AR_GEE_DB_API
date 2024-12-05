from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import TcStudents
from models import db

# 定義 Blueprint
tc_students_bp = Blueprint("tc_students_bp", __name__)

# 新增學生資料
@tc_students_bp.route("/tc_students", methods=["POST"])
def add_student():
    data = request.json
    new_student = TcStudents(
        student_id=data["student_id"],
        username=data["username"],
        password=data["password"],
        age=data["age"],
        disorder_category=data["disorder_category"],
        created_at=data["created_at"]
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# 查詢所有學生資料
@tc_students_bp.route("/tc_students", methods=["GET"])
def get_students():
    students = TcStudents.query.all()
    student_list = [{
        "student_id": student.student_id,
        "username": student.username,
        "password": student.password,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for student in students]
    return jsonify(student_list)

# 根據 student_id 查詢特定學生資料
@tc_students_bp.route("/tc_students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = TcStudents.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student_data = {
        "student_id": student.student_id,
        "username": student.username,
        "password": student.password,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(student_data)

# 更新學生資料
@tc_students_bp.route("/tc_students/<student_id>", methods=["PUT"])
def update_student(student_id):
    student = TcStudents.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.json
    student.username = data.get("username", student.username)
    student.password = data.get("password", student.password)
    student.age = data.get("age", student.age)
    student.disorder_category = data.get("disorder_category", student.disorder_category)
    student.created_at = data.get("created_at", student.created_at)

    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# 刪除學生資料
@tc_students_bp.route("/tc_students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = TcStudents.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})
