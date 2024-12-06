import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Answers
from models import db
from datetime import datetime

# 定義 Blueprint
answers_bp = Blueprint("answers_bp", __name__)

# 新增答案資料
@answers_bp.route("/answers", methods=["POST"])
def add_answer():
    data = request.json

    # 檢查必填欄位
    required_fields = ["student_id", "is_correct", "response_time", "incorrect_attempts"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # 生成唯一 answer_id
    generated_answer_id = f"answer_{uuid.uuid4().hex[:8]}"

    # 設定 test_date 為今天的日期
    test_date = datetime.now()

    # 建立答案資料
    new_answer = Answers(
        answer_id=generated_answer_id,
        student_id=data["student_id"],
        is_correct=data["is_correct"],
        response_time=data["response_time"],
        test_date=test_date,  # 使用今天的日期
        incorrect_attempts=data["incorrect_attempts"]
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({"message": "Answer added successfully", "answer_id": generated_answer_id}), 201

# 查詢所有答案資料
@answers_bp.route("/answers", methods=["GET"])
def get_answers():
    answers = Answers.query.all()
    answer_list = [{
        "answer_id": answer.answer_id,
        "student_id": answer.student_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "incorrect_attempts": answer.incorrect_attempts
    } for answer in answers]
    return jsonify(answer_list)

# 根據 answer_id 查詢特定答案
@answers_bp.route("/answers/<answer_id>", methods=["GET"])
def get_answer(answer_id):
    answer = Answers.query.get(answer_id)
    if not answer:
        return jsonify({"error": "Answer not found"}), 404
    answer_data = {
        "answer_id": answer.answer_id,
        "student_id": answer.student_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "incorrect_attempts": answer.incorrect_attempts
    }
    return jsonify(answer_data)

# 更新答案資料
@answers_bp.route("/answers/<answer_id>", methods=["PUT"])
def update_answer(answer_id):
    answer = Answers.query.get(answer_id)
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    data = request.json
    answer.is_correct = data.get("is_correct", answer.is_correct)
    answer.response_time = data.get("response_time", answer.response_time)
    answer.test_date = data.get("test_date", answer.test_date)
    answer.incorrect_attempts = data.get("incorrect_attempts", answer.incorrect_attempts)

    db.session.commit()
    return jsonify({"message": "Answer updated successfully"})

# 刪除答案資料
@answers_bp.route("/answers/<answer_id>", methods=["DELETE"])
def delete_answer(answer_id):
    answer = Answers.query.get(answer_id)
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "Answer deleted successfully"})
