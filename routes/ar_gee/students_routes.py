from flask import Blueprint, request, jsonify
from models.ar_gee_model import Students
from models import db

# 定義 Blueprint
student_bp = Blueprint("student_bp", __name__)

# 新增學生資料
@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.json

    # 檢查必填欄位
    required_fields = ["student_id", "username", "age", "disorder_category", "created_at"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # 新增學生資料
    new_student = Students(
        student_id=data["student_id"],
        username=data["username"],
        age=data["age"],
        disorder_category=data["disorder_category"],
        created_at=data["created_at"]
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# 查詢所有學生資料
@student_bp.route("/students", methods=["GET"])
def get_students():
    students = Students.query.all()
    student_list = [{
        "student_id": student.student_id,
        "username": student.username,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for student in students]
    return jsonify(student_list)

# 根據 student_id 查詢特定學生
@student_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = Students.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student_data = {
        "student_id": student.student_id,
        "username": student.username,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(student_data)

# 更新學生資料
@student_bp.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    student = Students.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.json
    student.username = data.get("username", student.username)
    student.age = data.get("age", student.age)
    student.disorder_category = data.get("disorder_category", student.disorder_category)
    student.created_at = data.get("created_at", student.created_at)

    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# 刪除學生資料
@student_bp.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Students.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})
