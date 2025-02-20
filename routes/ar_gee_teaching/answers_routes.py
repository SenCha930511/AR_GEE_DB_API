import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Answers
from models import db
from datetime import datetime

# 定義 Blueprint
answers_bp = Blueprint("answers_bp", __name__)

@answers_bp.route("/answers", methods=["POST"])
def add_answers():
    """
    新增練習答案資料

    :return: Tuple[jsonify, int] - 回傳 JSON 格式的訊息與 HTTP 狀態碼
    """
    data = request.json
    
    # 生成唯一的 answer_id
    answer_id: str = f"answers_{uuid.uuid4().hex[:8]}"
    
    # 設定 test_date 為今天的日期
    test_date: datetime = datetime.now()
    
    # 將秒數轉換為 HH:MM:SS 格式
    total_seconds: float = data["response_time"]
    hours: int = int(total_seconds // 3600)
    minutes: int = int((total_seconds % 3600) // 60)
    seconds: int = int(total_seconds % 60)
    formatted_response_time: str = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    # 建立新的練習答案實例
    new_answer: Answers = Answers(
        answer_id=answer_id,
        student_id=data["student_id"],
        question_id=data["question_id"],
        is_correct=data["is_correct"],
        response_time=formatted_response_time,
        test_date=test_date,
        incorrect_attempts=data["incorrect_attempts"]
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({"message": "Answer added successfully", "answer_id": answer_id}), 201


@answers_bp.route("/answers", methods=["GET"])
def get_answers():
    """
    查詢所有練習答案資料

    :return: jsonify - 回傳所有練習答案資料的 JSON 列表
    """
    answers = Answers.query.all()
    answer_list = [{
        "answer_id": answer.answer_id,
        "student_id": answer.student_id,
        "question_id": answer.question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "incorrect_attempts": answer.incorrect_attempts
    } for answer in answers]
    return jsonify(answer_list)


@answers_bp.route("/answers/<student_id>/<question_id>", methods=["GET"])
def get_answer(student_id: str, question_id: str):
    """
    根據 student_id 和 question_id 查詢最新一筆練習答案資料

    :param student_id: str - 學生 ID
    :param question_id: str - 題目 ID
    :return: jsonify - 回傳查詢結果的 JSON 格式資料；若查無資料則回傳錯誤訊息
    """
    answer = Answers.query.filter(
        Answers.student_id == student_id,
        Answers.question_id == question_id
    ).order_by(Answers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Answer not found"}), 404
    
    answer_data = {
        "answer_id": answer.answer_id,
        "student_id": answer.student_id,
        "question_id": answer.question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),
        "incorrect_attempts": answer.incorrect_attempts
    }
    return jsonify(answer_data)


@answers_bp.route("/answers/<student_id>/<question_id>", methods=["PUT"])
def update_answer(student_id: str, question_id: str):
    """
    更新指定學生與題目的練習答案資料

    :param student_id: str - 學生 ID
    :param question_id: str - 題目 ID
    :return: jsonify - 回傳更新成功訊息；若查無資料則回傳錯誤訊息
    """
    answer = Answers.query.filter(
        Answers.student_id == student_id,
        Answers.question_id == question_id
    ).order_by(Answers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    data = request.json
    answer.is_correct = data.get("is_correct", answer.is_correct)
    answer.response_time = data.get("response_time", answer.response_time)
    answer.test_date = data.get("test_date", answer.test_date)  # 可選擇不修改日期
    answer.incorrect_attempts = data.get("incorrect_attempts", answer.incorrect_attempts)

    db.session.commit()
    return jsonify({"message": "Answer updated successfully"})


@answers_bp.route("/answers/<student_id>/<question_id>", methods=["DELETE"])
def delete_answer(student_id: str, question_id: str):
    """
    刪除指定學生與題目的練習答案資料

    :param student_id: str - 學生 ID
    :param question_id: str - 題目 ID
    :return: jsonify - 回傳刪除成功訊息；若查無資料則回傳錯誤訊息
    """
    answer = Answers.query.filter(
        Answers.student_id == student_id,
        Answers.question_id == question_id
    ).order_by(Answers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "Answer deleted successfully"})
