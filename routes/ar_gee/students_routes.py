import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_model import Students
from models import db
from datetime import datetime

# 定義 Blueprint
student_bp = Blueprint("student_bp", __name__)

# 新增學生資料
@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.json

    # 生成唯一 student_id
    student_id = f"student_{uuid.uuid4().hex[:8]}"

    # 檢查必填欄位
    required_fields = ["username", "age", "disorder_category"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # 設定創建時間
    created_at = datetime.now()

    # 新增學生資料
    new_student = Students(
        student_id=student_id,
        username=data["username"],
        age=data["age"],
        disorder_category=data["disorder_category"],
        created_at=created_at
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully", "student_id": student_id}), 201

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

    # 更新創建時間
    if "created_at" in data:
        try:
            student.created_at = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

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
