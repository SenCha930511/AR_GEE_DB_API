from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Statistics
from models import db

# 定義 Blueprint
statistics_bp = Blueprint("statistics_bp", __name__)

@statistics_bp.route("/statistics", methods=["POST"])
def add_statistic():
    """
    新增統計資料

    從請求中取得統計資料並建立新的統計記錄。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201
    """
    data = request.json
    new_stat: Statistics = Statistics(
        student_id=data["student_id"],
        unit_id=data["unit_id"],
        total_correct=data["total_correct"],
        total_questions=data["total_questions"],
        accuracy_rate=data["accuracy_rate"]
    )
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({"message": "Statistic added successfully"}), 201


@statistics_bp.route("/statistics", methods=["GET"])
def get_statistics():
    """
    查詢所有統計資料

    :return: jsonify - 回傳所有統計資料的 JSON 列表
    """
    stats = Statistics.query.all()
    stat_list = [{
        "student_id": stat.student_id,
        "unit_id": stat.unit_id,
        "total_correct": stat.total_correct,
        "total_questions": stat.total_questions,
        "accuracy_rate": stat.accuracy_rate
    } for stat in stats]
    return jsonify(stat_list)


@statistics_bp.route("/statistics/<student_id>/<unit_id>", methods=["GET"])
def get_statistic(student_id: str, unit_id: str):
    """
    根據 student_id 與 unit_id 查詢特定統計資料

    :param student_id: str - 學生 ID
    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳特定統計資料的 JSON 格式；若查無資料則回傳錯誤訊息
    """
    stat: Statistics = Statistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Statistic not found"}), 404
    stat_data = {
        "student_id": stat.student_id,
        "unit_id": stat.unit_id,
        "total_correct": stat.total_correct,
        "total_questions": stat.total_questions,
        "accuracy_rate": stat.accuracy_rate
    }
    return jsonify(stat_data)


@statistics_bp.route("/statistics/<student_id>/<unit_id>", methods=["PUT"])
def update_statistic(student_id: str, unit_id: str):
    """
    更新指定統計資料

    根據 student_id 與 unit_id 更新統計記錄。

    :param student_id: str - 學生 ID
    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳更新成功訊息；若查無資料則回傳錯誤訊息
    """
    stat: Statistics = Statistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Statistic not found"}), 404

    data = request.json
    stat.total_correct = data.get("total_correct", stat.total_correct)
    stat.total_questions = data.get("total_questions", stat.total_questions)
    stat.accuracy_rate = data.get("accuracy_rate", stat.accuracy_rate)

    db.session.commit()
    return jsonify({"message": "Statistic updated successfully"})


@statistics_bp.route("/statistics/<student_id>/<unit_id>", methods=["DELETE"])
def delete_statistic(student_id: str, unit_id: str):
    """
    刪除指定統計資料

    根據 student_id 與 unit_id 刪除統計記錄。

    :param student_id: str - 學生 ID
    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳刪除成功訊息；若查無資料則回傳錯誤訊息
    """
    stat: Statistics = Statistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Statistic not found"}), 404

    db.session.delete(stat)
    db.session.commit()
    return jsonify({"message": "Statistic deleted successfully"})
