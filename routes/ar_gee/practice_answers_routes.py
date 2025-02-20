import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeAnswers
from models import db
from datetime import datetime

# 定義 Blueprint
practice_answers_bp = Blueprint("practice_answers_bp", __name__)

@practice_answers_bp.route("/practice_answers", methods=["POST"])
def add_practice_answer():
    """
    新增練習答案資料

    從請求 JSON 中解析練習答案資料，生成唯一的 practice_answer_id 並設定 test_date，
    將 response_time 轉換為 HH:MM:SS 格式，建立新的練習答案記錄並儲存至資料庫。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201
    """
    data = request.json
    # 生成唯一的 practice_answer_id
    practice_answer_id: str = f"practice_answer_{uuid.uuid4().hex[:8]}"

    # 設定 test_date 為今天的日期
    test_date: datetime = datetime.now()
     
    total_seconds: float = data["response_time"]
    hours: int = int(total_seconds // 3600)
    minutes: int = int((total_seconds % 3600) // 60)
    seconds: int = int(total_seconds % 60)
    formatted_response_time: str = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    # 建立新的練習答案實例
    new_answer: PracticeAnswers = PracticeAnswers(
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


@practice_answers_bp.route("/practice_answers", methods=["GET"])
def get_practice_answers():
    """
    查詢所有練習答案資料

    從資料庫中查詢所有練習答案記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有練習答案資料的 JSON 列表
    """
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


@practice_answers_bp.route("/practice_answers/<student_id>&<question_id>", methods=["GET"])
def get_practice_answer(student_id: str, question_id: str):
    """
    根據 student_id 與 practice_question_id 查詢最新一筆練習答案資料

    :param student_id: str - 學生 ID
    :param question_id: str - 練習題目 ID
    :return: jsonify - 回傳該練習答案的 JSON 格式資料；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    answer = PracticeAnswers.query.filter(
        PracticeAnswers.student_id == student_id,
        PracticeAnswers.practice_question_id == question_id
    ).order_by(PracticeAnswers.test_date.desc()).first()
    
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


@practice_answers_bp.route("/practice_answers/<student_id>&<question_id>", methods=["PUT"])
def update_practice_answer(student_id: str, question_id: str):
    """
    更新練習答案資料

    根據 student_id 與 practice_question_id 更新練習答案記錄，若查無資料則回傳錯誤訊息。

    :param student_id: str - 學生 ID
    :param question_id: str - 練習題目 ID
    :return: jsonify - 回傳更新成功訊息；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    answer = PracticeAnswers.query.filter(
        PracticeAnswers.student_id == student_id,
        PracticeAnswers.practice_question_id == question_id
    ).order_by(PracticeAnswers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404

    data = request.json
    answer.is_correct = data.get("is_correct", answer.is_correct)
    answer.response_time = data.get("response_time", answer.response_time)
    answer.test_date = data.get("test_date", answer.test_date)
    answer.incorrect_attempts = data.get("incorrect_attempts", answer.incorrect_attempts)

    db.session.commit()
    return jsonify({"message": "Practice answer updated successfully"})


@practice_answers_bp.route("/practice_answers/<student_id>&<question_id>", methods=["DELETE"])
def delete_practice_answer(student_id: str, question_id: str):
    """
    刪除練習答案資料

    根據 student_id 與 practice_question_id 刪除練習答案記錄，若查無資料則回傳錯誤訊息。

    :param student_id: str - 學生 ID
    :param question_id: str - 練習題目 ID
    :return: jsonify - 回傳刪除成功訊息；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    answer = PracticeAnswers.query.filter(
        PracticeAnswers.student_id == student_id,
        PracticeAnswers.practice_question_id == question_id
    ).order_by(PracticeAnswers.test_date.desc()).first()
    
    if not answer:
        return jsonify({"error": "Practice answer not found"}), 404

    db.session.delete(answer)
    db.session.commit()
    return jsonify({"message": "Practice answer deleted successfully"})
