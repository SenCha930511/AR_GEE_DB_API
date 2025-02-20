import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Questions
from models import db

# 定義 Blueprint
questions_bp = Blueprint("questions_bp", __name__)

@questions_bp.route("/questions", methods=["POST"])
def add_question():
    """
    新增問題資料

    :return: Tuple[jsonify, int] - 回傳 JSON 格式的訊息與 HTTP 狀態碼
    """
    data = request.json

    # 檢查必填欄位
    if not data.get("unit_id"):
        return jsonify({"error": "Missing required field: unit_id"}), 400

    # 生成唯一 question_id
    generated_question_id: str = f"question_{uuid.uuid4().hex[:8]}"

    # 建立問題資料
    new_question: Questions = Questions(
        question_id=generated_question_id,
        unit_id=data["unit_id"]
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"message": "Question added successfully", "question_id": generated_question_id}), 201


@questions_bp.route("/questions", methods=["GET"])
def get_questions():
    """
    查詢所有問題資料

    :return: jsonify - 回傳所有問題資料的 JSON 列表
    """
    questions = Questions.query.all()
    question_list = [{
        "question_id": question.question_id,
        "unit_id": question.unit_id
    } for question in questions]
    return jsonify(question_list)


@questions_bp.route("/questions/<question_id>", methods=["GET"])
def get_question(question_id: str):
    """
    根據 question_id 查詢特定問題資料

    :param question_id: str - 問題 ID
    :return: jsonify - 回傳特定問題資料的 JSON 格式；若查無資料則回傳錯誤訊息
    """
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    question_data = {
        "question_id": question.question_id,
        "unit_id": question.unit_id
    }
    return jsonify(question_data)


@questions_bp.route("/questions/<question_id>", methods=["PUT"])
def update_question(question_id: str):
    """
    更新指定問題資料

    :param question_id: str - 問題 ID
    :return: jsonify - 回傳更新成功訊息；若查無資料則回傳錯誤訊息
    """
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.json
    question.unit_id = data.get("unit_id", question.unit_id)

    db.session.commit()
    return jsonify({"message": "Question updated successfully"})


@questions_bp.route("/questions/<question_id>", methods=["DELETE"])
def delete_question(question_id: str):
    """
    刪除指定問題資料

    :param question_id: str - 問題 ID
    :return: jsonify - 回傳刪除成功訊息；若查無資料則回傳錯誤訊息
    """
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"})
