import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeQuestions
from models import db

# 定義 Blueprint
practice_questions_bp = Blueprint("practice_questions_bp", __name__)

@practice_questions_bp.route("/practice_questions", methods=["POST"])
def add_practice_question():
    """
    新增練習題目

    從請求 JSON 中解析練習題目資料，生成唯一的 practice_question_id，
    建立新的練習題目記錄並儲存至資料庫。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201
    """
    data = request.json
    # 生成唯一的 practice_question_id
    practice_question_id: str = f"practice_question_{uuid.uuid4().hex[:8]}"

    new_question: PracticeQuestions = PracticeQuestions(
        practice_question_id=practice_question_id,
        unit_id=data["unit_id"]
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({
        "message": "Practice question added successfully",
        "practice_question_id": practice_question_id
    }), 201


@practice_questions_bp.route("/practice_questions", methods=["GET"])
def get_practice_questions():
    """
    查詢所有練習題目

    從資料庫中查詢所有練習題目記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有練習題目資料的 JSON 列表
    """
    questions = PracticeQuestions.query.all()
    question_list = [{
        "practice_question_id": question.practice_question_id,
        "unit_id": question.unit_id
    } for question in questions]
    return jsonify(question_list)


@practice_questions_bp.route("/practice_questions/<practice_question_id>", methods=["GET"])
def get_practice_question(practice_question_id: str):
    """
    根據 practice_question_id 查詢特定練習題目

    :param practice_question_id: str - 練習題目 ID
    :return: jsonify - 回傳該練習題目的 JSON 格式資料；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    question = PracticeQuestions.query.get(practice_question_id)
    if not question:
        return jsonify({"error": "Practice question not found"}), 404
    question_data = {
        "practice_question_id": question.practice_question_id,
        "unit_id": question.unit_id
    }
    return jsonify(question_data)


@practice_questions_bp.route("/practice_questions/<practice_question_id>", methods=["PUT"])
def update_practice_question(practice_question_id: str):
    """
    更新練習題目資料

    根據 practice_question_id 更新練習題目記錄，若查無該記錄則回傳錯誤訊息。

    :param practice_question_id: str - 練習題目 ID
    :return: jsonify - 回傳更新成功訊息；若查無該記錄則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    question = PracticeQuestions.query.get(practice_question_id)
    if not question:
        return jsonify({"error": "Practice question not found"}), 404

    data = request.json
    question.unit_id = data.get("unit_id", question.unit_id)

    db.session.commit()
    return jsonify({"message": "Practice question updated successfully"})


@practice_questions_bp.route("/practice_questions/<practice_question_id>", methods=["DELETE"])
def delete_practice_question(practice_question_id: str):
    """
    刪除練習題目

    根據 practice_question_id 刪除練習題目記錄，若查無該記錄則回傳錯誤訊息。

    :param practice_question_id: str - 練習題目 ID
    :return: jsonify - 回傳刪除成功訊息；若查無該記錄則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    question = PracticeQuestions.query.get(practice_question_id)
    if not question:
        return jsonify({"error": "Practice question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Practice question deleted successfully"})
