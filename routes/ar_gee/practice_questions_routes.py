from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeQuestions
from models import db

# 定義 Blueprint
practice_questions_bp = Blueprint("practice_questions_bp", __name__)

# 新增練習題目
@practice_questions_bp.route("/practice_questions", methods=["POST"])
def add_practice_question():
    data = request.json
    new_question = PracticeQuestions(
        practice_question_id=data["practice_question_id"],
        unit_id=data["unit_id"]
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"message": "Practice question added successfully"}), 201

# 查詢所有練習題目
@practice_questions_bp.route("/practice_questions", methods=["GET"])
def get_practice_questions():
    questions = PracticeQuestions.query.all()
    question_list = [{
        "practice_question_id": question.practice_question_id,
        "unit_id": question.unit_id
    } for question in questions]
    return jsonify(question_list)

# 根據 practice_question_id 查詢特定練習題目
@practice_questions_bp.route("/practice_questions/<practice_question_id>", methods=["GET"])
def get_practice_question(practice_question_id):
    question = PracticeQuestions.query.get(practice_question_id)
    if not question:
        return jsonify({"error": "Practice question not found"}), 404
    question_data = {
        "practice_question_id": question.practice_question_id,
        "unit_id": question.unit_id
    }
    return jsonify(question_data)

# 更新練習題目資料
@practice_questions_bp.route("/practice_questions/<practice_question_id>", methods=["PUT"])
def update_practice_question(practice_question_id):
    question = PracticeQuestions.query.get(practice_question_id)
    if not question:
        return jsonify({"error": "Practice question not found"}), 404

    data = request.json
    question.unit_id = data.get("unit_id", question.unit_id)
    
    db.session.commit()
    return jsonify({"message": "Practice question updated successfully"})

# 刪除練習題目
@practice_questions_bp.route("/practice_questions/<practice_question_id>", methods=["DELETE"])
def delete_practice_question(practice_question_id):
    question = PracticeQuestions.query.get(practice_question_id)
    if not question:
        return jsonify({"error": "Practice question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Practice question deleted successfully"})
