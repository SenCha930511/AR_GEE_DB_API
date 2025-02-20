import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import TcStudents
from models import db
from datetime import datetime

# 定義 Blueprint
tc_students_bp = Blueprint("tc_students_bp", __name__)

@tc_students_bp.route("/tc_students", methods=["POST"])
def add_student():
    """
    新增學生資料

    從請求 JSON 中解析學生資料，檢查必填欄位、解析 birth_date（若提供），
    生成唯一的 student_id 並設定 created_at 為當前時間，建立並儲存新的學生記錄。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201；若缺少必填欄位則回傳錯誤訊息與 HTTP 狀態碼 400
    """
    data = request.json

    # 檢查必填欄位
    required_fields = ["name", "age", "disorder_category", "gender"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # 解析 birth_date，如果提供的話
    birth_date_input = data.get("birth_date")
    if birth_date_input:
        birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d").date()
    else:
        birth_date = None

    # 生成唯一 student_id
    generated_student_id: str = f"student_{uuid.uuid4().hex[:8]}"

    # 設定 created_at 為當前時間
    created_at: datetime = datetime.now()

    # 建立新的學生記錄
    new_student: TcStudents = TcStudents(
        student_id=generated_student_id,
        name=data["name"],
        gender=data["gender"],
        birth_date=birth_date,
        age=data["age"],
        disorder_category=data["disorder_category"],
        created_at=created_at
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully", "student_id": generated_student_id}), 201


@tc_students_bp.route("/tc_students", methods=["GET"])
def get_students():
    """
    查詢所有學生資料

    從資料庫中查詢所有學生記錄，並以 JSON 列表格式回傳。

    :return: Tuple[jsonify, int] - 回傳學生資料列表與 HTTP 狀態碼 200
    """
    students = TcStudents.query.all()
    student_list = [{
        "student_id": student.student_id,
        "name": student.name,
        "gender": student.gender,
        "birth_date": student.birth_date.strftime("%Y-%m-%d") if student.birth_date else None,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for student in students]
    return jsonify(student_list), 200


@tc_students_bp.route("/tc_students/<student_id>", methods=["GET"])
def get_student(student_id: str):
    """
    根據 student_id 查詢特定學生資料

    :param student_id: str - 學生 ID
    :return: Tuple[jsonify, int] - 回傳該學生的 JSON 格式資料與 HTTP 狀態碼 200；若查無該學生則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    student = TcStudents.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student_data = {
        "student_id": student.student_id,
        "name": student.name,
        "gender": student.gender,
        "birth_date": student.birth_date.strftime("%Y-%m-%d") if student.birth_date else None,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(student_data), 200


@tc_students_bp.route("/tc_students/<student_id>", methods=["PUT"])
def update_student(student_id: str):
    """
    更新指定學生資料

    根據 student_id 更新學生記錄。若未查詢到該學生，回傳錯誤訊息。

    :param student_id: str - 學生 ID
    :return: Tuple[jsonify, int] - 回傳更新成功訊息與 HTTP 狀態碼 200；若查無該學生則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    student = TcStudents.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.json
    student.name = data.get("name", student.name)
    student.gender = data.get("gender", student.gender)
    
    # 更新 birth_date
    birth_date_input = data.get("birth_date")
    if birth_date_input:
        student.birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d").date()
    else:
        student.birth_date = None

    student.age = data.get("age", student.age)
    student.disorder_category = data.get("disorder_category", student.disorder_category)

    db.session.commit()
    return jsonify({"message": "Student updated successfully"}), 200


@tc_students_bp.route("/tc_students/<student_id>", methods=["DELETE"])
def delete_student(student_id: str):
    """
    刪除指定學生資料

    根據 student_id 刪除學生記錄。

    :param student_id: str - 學生 ID
    :return: Tuple[jsonify, int] - 回傳刪除成功訊息與 HTTP 狀態碼 200；若查無該學生則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    student = TcStudents.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200
