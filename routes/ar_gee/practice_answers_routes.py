from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeAnswers
from models import db
import uuid
from datetime import datetime

# 定義 Blueprint
practice_answers_bp = Blueprint("practice_answers_bp", __name__)

# 新增練習答案資料
@practice_answers_bp.route("/practice_answers", methods=["POST"])
def add_practice_answer():
    data = request.json
    # 生成唯一的 practice_answer_id
    practice_answer_id = f"practice_answer_{uuid.uuid4().hex[:8]}"

    # 設定 test_date 為今天的日期
    test_date = datetime.now()
     
    total_seconds = data["response_time"]
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    formatted_response_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    print(formatted_response_time)

    # 建立新的練習答案實例
    new_answer = PracticeAnswers(
        practice_answer_id=practice_answer_id,
        student_id=data["student_id"],
        practice_question_id=data["practice_question_id"],
        is_correct=data["is_correct"],
        response_time=formatted_response_time,
        test_date=test_date,
        incorrect_attempts=data["incorrect_attempts"]
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({"message": "Practice answer added successfully", "practice_answer_id": practice_answer_id}), 201

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
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化 test_date
        "incorrect_attempts": answer.incorrect_attempts
    } for answer in answers]
    return jsonify(answer_list)

# 根據 student_id 和 question_id 查詢練習答案資料
@practice_answers_bp.route("/practice_answers/<student_id>&<question_id>", methods=["GET"])
def get_practice_answer(student_id, question_id):
    answer = PracticeAnswers.query.filter(
        PracticeAnswers.student_id == student_id,
        PracticeAnswers.practice_question_id == question_id  # 使用 question_id 作為過濾條件
    ).order_by(PracticeAnswers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404
    
    answer_data = {
        "practice_answer_id": answer.practice_answer_id,
        "student_id": answer.student_id,
        "practice_question_id": answer.practice_question_id,
        "is_correct": answer.is_correct,
        "response_time": str(answer.response_time),
        "test_date": answer.test_date.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化 test_date
        "incorrect_attempts": answer.incorrect_attempts
    }
    return jsonify(answer_data)

# 更新練習答案資料
@practice_answers_bp.route("/practice_answers/<student_id>&<question_id>", methods=["PUT"])
def update_practice_answer(student_id, question_id):
    answer = PracticeAnswers.query.filter(
        PracticeAnswers.student_id == student_id,
        PracticeAnswers.practice_question_id == question_id  # 使用 question_id 作為過濾條件
    ).order_by(PracticeAnswers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404

    data = request.json
    answer.is_correct = data.get("is_correct", answer.is_correct)
    answer.response_time = data.get("response_time", answer.response_time)
    answer.test_date = data.get("test_date", answer.test_date)  # 可以選擇不修改日期
    answer.incorrect_attempts = data.get("incorrect_attempts", answer.incorrect_attempts)

    db.session.commit()
    return jsonify({"message": "Practice answer updated successfully"})

# 刪除練習答案資料
@practice_answers_bp.route("/practice_answers/<student_id>&<question_id>", methods=["DELETE"])
def delete_practice_answer(student_id, question_id):
    answer = PracticeAnswers.query.filter(
        PracticeAnswers.student_id == student_id,
        PracticeAnswers.practice_question_id == question_id  # 使用 question_id 作為過濾條件
    ).order_by(PracticeAnswers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "Practice answer deleted successfully"})
