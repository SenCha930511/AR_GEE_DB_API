from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeAnswers
from models import db

# 定義 Blueprint
practice_answers_bp = Blueprint("practice_answers_bp", __name__)

# 新增練習答案資料
@practice_answers_bp.route("/practice_answers", methods=["POST"])
def add_practice_answer():
    data = request.json
    new_answer = PracticeAnswers(
        practice_answer_id=data["practice_answer_id"],
        student_id=data["student_id"],
        practice_question_id=data["practice_question_id"],
        is_correct=data["is_correct"],
        response_time=data["response_time"],
        test_date=data["test_date"],
        incorrect_attempts=data["incorrect_attempts"]
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({"message": "Practice answer added successfully"}), 201

# 查詢所有練習答案資料
@practice_answers_bp.route("/practice_answers", methods=["GET"])
def get_practice_answers():
    answers = PracticeAnswers.query.all()
    answer_list = [{
        "practice_answer_id": answer.practice_answer_id,
        "student_id": answer.student_id,
        "practice_question_id": answer.practice_question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "incorrect_attempts": answer.incorrect_attempts
    } for answer in answers]
    return jsonify(answer_list)

# 根據 practice_answer_id 查詢特定練習答案
@practice_answers_bp.route("/practice_answers/<practice_answer_id>", methods=["GET"])
def get_practice_answer(practice_answer_id):
    answer = PracticeAnswers.query.get(practice_answer_id)
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404
    answer_data = {
        "practice_answer_id": answer.practice_answer_id,
        "student_id": answer.student_id,
        "practice_question_id": answer.practice_question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "incorrect_attempts": answer.incorrect_attempts
    }
    return jsonify(answer_data)

# 更新練習答案資料
@practice_answers_bp.route("/practice_answers/<practice_answer_id>", methods=["PUT"])
def update_practice_answer(practice_answer_id):
    answer = PracticeAnswers.query.get(practice_answer_id)
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404

    data = request.json
    answer.is_correct = data.get("is_correct", answer.is_correct)
    answer.response_time = data.get("response_time", answer.response_time)
    answer.test_date = data.get("test_date", answer.test_date)
    answer.incorrect_attempts = data.get("incorrect_attempts", answer.incorrect_attempts)

    db.session.commit()
    return jsonify({"message": "Practice answer updated successfully"})

# 刪除練習答案資料
@practice_answers_bp.route("/practice_answers/<practice_answer_id>", methods=["DELETE"])
def delete_practice_answer(practice_answer_id):
    answer = PracticeAnswers.query.get(practice_answer_id)
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "Practice answer deleted successfully"})
