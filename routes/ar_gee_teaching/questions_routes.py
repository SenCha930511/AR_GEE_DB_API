from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Questions
from models import db

# 定義 Blueprint
questions_bp = Blueprint("questions_bp", __name__)

# 新增問題資料
@questions_bp.route("/questions", methods=["POST"])
def add_question():
    data = request.json
    new_question = Questions(
        question_id=data["question_id"],
        unit_id=data["unit_id"]
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"message": "Question added successfully"}), 201

# 查詢所有問題資料
@questions_bp.route("/questions", methods=["GET"])
def get_questions():
    questions = Questions.query.all()
    question_list = [{
        "question_id": question.question_id,
        "unit_id": question.unit_id
    } for question in questions]
    return jsonify(question_list)

# 根據 question_id 查詢特定問題
@questions_bp.route("/questions/<question_id>", methods=["GET"])
def get_question(question_id):
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    question_data = {
        "question_id": question.question_id,
        "unit_id": question.unit_id
    }
    return jsonify(question_data)

# 更新問題資料
@questions_bp.route("/questions/<question_id>", methods=["PUT"])
def update_question(question_id):
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.json
    question.unit_id = data.get("unit_id", question.unit_id)

    db.session.commit()
    return jsonify({"message": "Question updated successfully"})

# 刪除問題資料
@questions_bp.route("/questions/<question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"})
