import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Answers
from models import db
from datetime import datetime

# 定義 Blueprint
answers_bp = Blueprint("answers_bp", __name__)

# 新增練習答案資料
@answers_bp.route("/answers", methods=["POST"])
def add_answers():
    data = request.json
    
    # 生成唯一的 answer_id
    answer_id = f"answers_{uuid.uuid4().hex[:8]}"

    # 設定 test_date 為今天的日期
    test_date = datetime.now()
     
    total_seconds = data["response_time"]
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    formatted_response_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    print(formatted_response_time)

    # 建立新的練習答案實例
    new_answer = Answers(
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

# 查詢所有練習答案資料
@answers_bp.route("/answers", methods=["GET"])
def get_answers():
    answers = Answers.query.all()
    answer_list = [{
        "answer_id": answer.answer_id,
        "student_id": answer.student_id,
        "question_id": answer.question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化 test_date
        "incorrect_attempts": answer.incorrect_attempts
    } for answer in answers]
    return jsonify(answer_list)

# 根據 student_id 和 question_id 查詢練習答案資料
@answers_bp.route("/answers/<student_id>/<question_id>", methods=["GET"])
def get_answer(student_id, question_id):
    answer = Answers.query.filter(
        Answers.student_id == student_id,
        Answers.question_id == question_id  # 使用 question_id 作為過濾條件
    ).order_by(Answers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Answer not found"}), 404
    
    answer_data = {
        "answer_id": answer.answer_id,
        "student_id": answer.student_id,
        "question_id": answer.question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化 test_date
        "incorrect_attempts": answer.incorrect_attempts
    }
    return jsonify(answer_data)

# 更新練習答案資料
@answers_bp.route("/answers/<student_id>/<question_id>", methods=["PUT"])
def update_answer(student_id, question_id):
    answer = Answers.query.filter(
        Answers.student_id == student_id,
        Answers.question_id == question_id  # 使用 question_id 作為過濾條件
    ).order_by(Answers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    data = request.json
    answer.is_correct = data.get("is_correct", answer.is_correct)
    answer.response_time = data.get("response_time", answer.response_time)
    answer.test_date = data.get("test_date", answer.test_date)  # 可以選擇不修改日期
    answer.incorrect_attempts = data.get("incorrect_attempts", answer.incorrect_attempts)

    db.session.commit()
    return jsonify({"message": "Answer updated successfully"})

# 刪除練習答案資料
@answers_bp.route("/answers/<student_id>/<question_id>", methods=["DELETE"])
def delete_answer(student_id, question_id):
    answer = Answers.query.filter(
        Answers.student_id == student_id,
        Answers.question_id == question_id  # 使用 question_id 作為過濾條件
    ).order_by(Answers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "Answer deleted successfully"})
