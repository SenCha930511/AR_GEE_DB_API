import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_model import Students
from models import db
from datetime import datetime

# 定義 Blueprint
student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/students", methods=["POST"])
def add_student():
    """
    新增學生資料

    從請求 JSON 中解析學生資料，生成唯一的 student_id，
    檢查必填欄位 (username, age, disorder_category) 是否存在，
    設定創建時間並建立新的學生記錄，儲存至資料庫。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201；
             若缺少必填欄位則回傳錯誤訊息與 HTTP 狀態碼 400
    """
    data = request.json

    # 生成唯一 student_id
    student_id: str = f"student_{uuid.uuid4().hex[:8]}"

    # 檢查必填欄位
    required_fields = ["username", "age", "disorder_category"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # 設定創建時間
    created_at: datetime = datetime.now()

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


@student_bp.route("/students", methods=["GET"])
def get_students():
    """
    查詢所有學生資料

    從資料庫中查詢所有學生記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有學生資料的 JSON 列表
    """
    students = Students.query.all()
    student_list = [{
        "student_id": student.student_id,
        "username": student.username,
        "age": student.age,
        "disorder_category": student.disorder_category,
        "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for student in students]
    return jsonify(student_list)


@student_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id: str):
    """
    根據 student_id 查詢特定學生資料

    根據 student_id 從資料庫中查詢學生記錄。

    :param student_id: str - 學生 ID
    :return: jsonify - 回傳該學生的 JSON 格式資料；
             若查無學生則回傳錯誤訊息與 HTTP 狀態碼 404
    """
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


@student_bp.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id: str):
    """
    更新學生資料

    根據 student_id 更新學生記錄。若提供 created_at 則會驗證日期格式，
    更新學生的 username、age、disorder_category 與創建時間。

    :param student_id: str - 學生 ID
    :return: Tuple[jsonify, int] - 回傳更新成功訊息與 HTTP 狀態碼 200；
             若查無學生則回傳錯誤訊息與 HTTP 狀態碼 404，
             或若日期格式錯誤則回傳錯誤訊息與 HTTP 狀態碼 400
    """
    student = Students.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.json
    student.username = data.get("username", student.username)
    student.age = data.get("age", student.age)
    student.disorder_category = data.get("disorder_category", student.disorder_category)

    # 更新創建時間，如果有提供 created_at
    if "created_at" in data:
        try:
            student.created_at = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

    db.session.commit()
    return jsonify({"message": "Student updated successfully"})


@student_bp.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id: str):
    """
    刪除學生資料

    根據 student_id 從資料庫中刪除學生記錄。

    :param student_id: str - 學生 ID
    :return: Tuple[jsonify, int] - 回傳刪除成功訊息與 HTTP 狀態碼 200；
             若查無學生則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    student = Students.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})
