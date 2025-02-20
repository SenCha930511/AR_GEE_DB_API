from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeStatistics
from models import db

# 定義 Blueprint
practice_statistics_bp = Blueprint("practice_statistics_bp", __name__)

@practice_statistics_bp.route("/practice_statistics", methods=["POST"])
def add_practice_statistic():
    """
    新增練習統計資料

    從請求 JSON 中解析練習統計資料，建立新的練習統計記錄。
    若 total_questions 未提供，則使用預設值 3，將資料儲存至資料庫。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201
    """
    data = request.json
    new_stat: PracticeStatistics = PracticeStatistics(
        student_id=data["student_id"],
        unit_id=data["unit_id"],
        total_correct=data["total_correct"],
        total_questions=data.get("total_questions", 3),
        accuracy_rate=data["accuracy_rate"]
    )
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({"message": "Practice statistics added successfully"}), 201


@practice_statistics_bp.route("/practice_statistics", methods=["GET"])
def get_practice_statistics():
    """
    查詢所有練習統計資料

    從資料庫中查詢所有練習統計記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有練習統計資料的 JSON 列表
    """
    stats = PracticeStatistics.query.all()
    stat_list = [{
        "student_id": stat.student_id,
        "unit_id": stat.unit_id,
        "total_correct": stat.total_correct,
        "total_questions": stat.total_questions,
        "accuracy_rate": stat.accuracy_rate
    } for stat in stats]
    return jsonify(stat_list)


@practice_statistics_bp.route("/practice_statistics/<student_id>", methods=["GET"])
def get_practice_statistic(student_id: str):
    """
    根據 student_id 查詢特定學生的練習統計資料

    :param student_id: str - 學生 ID
    :return: jsonify - 回傳該學生所有練習統計資料的 JSON 列表；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    stats = PracticeStatistics.query.filter_by(student_id=student_id).all()
    if not stats:
        return jsonify({"error": "Practice statistics not found for student"}), 404
    stat_list = [{
        "unit_id": stat.unit_id,
        "total_correct": stat.total_correct,
        "total_questions": stat.total_questions,
        "accuracy_rate": stat.accuracy_rate
    } for stat in stats]
    return jsonify(stat_list)


@practice_statistics_bp.route("/practice_statistics/<student_id>/<unit_id>", methods=["PUT"])
def update_practice_statistic(student_id: str, unit_id: str):
    """
    更新練習統計資料

    根據 student_id 與 unit_id 更新練習統計記錄，
    若查無資料則回傳錯誤訊息。

    :param student_id: str - 學生 ID
    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳更新成功訊息；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    stat = PracticeStatistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Practice statistics not found"}), 404

    data = request.json
    stat.total_correct = data.get("total_correct", stat.total_correct)
    stat.total_questions = data.get("total_questions", stat.total_questions)
    stat.accuracy_rate = data.get("accuracy_rate", stat.accuracy_rate)

    db.session.commit()
    return jsonify({"message": "Practice statistics updated successfully"})


@practice_statistics_bp.route("/practice_statistics/<student_id>/<unit_id>", methods=["DELETE"])
def delete_practice_statistic(student_id: str, unit_id: str):
    """
    刪除練習統計資料

    根據 student_id 與 unit_id 刪除練習統計記錄，
    若查無資料則回傳錯誤訊息。

    :param student_id: str - 學生 ID
    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳刪除成功訊息；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    stat = PracticeStatistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Practice statistics not found"}), 404

    db.session.delete(stat)
    db.session.commit()
    return jsonify({"message": "Practice statistics deleted successfully"})
