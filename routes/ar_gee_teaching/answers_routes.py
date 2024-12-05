from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Answers
from models import db

# 定義 Blueprint
answers_bp = Blueprint("answers_bp", __name__)

# 新增答案資料
@answers_bp.route("/answers", methods=["POST"])
def add_answer():
    data = request.json
    new_answer = Answers(
        answer_id=data["answer_id"],
        student_id=data["student_id"],
        is_correct=data["is_correct"],
        response_time=data["response_time"],
        test_date=data["test_date"],
        incorrect_attempts=data["incorrect_attempts"]
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({"message": "Answer added successfully"}), 201

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
