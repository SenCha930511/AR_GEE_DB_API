from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeStatistics
from models import db

# 定義 Blueprint
practice_statistics_bp = Blueprint("practice_statistics_bp", __name__)

# 新增練習統計資料
@practice_statistics_bp.route("/practice_statistics", methods=["POST"])
def add_practice_statistic():
    data = request.json
    new_stat = PracticeStatistics(
        student_id=data["student_id"],
        unit_id=data["unit_id"],
        total_correct=data["total_correct"],
        total_questions=data.get("total_questions", 3),  # 默認值為 3
        accuracy_rate=data["accuracy_rate"]
    )
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({"message": "Practice statistics added successfully"}), 201

# 查詢所有練習統計資料
@practice_statistics_bp.route("/practice_statistics", methods=["GET"])
def get_practice_statistics():
    stats = PracticeStatistics.query.all()
    stat_list = [{
        "student_id": stat.student_id,
        "unit_id": stat.unit_id,
        "total_correct": stat.total_correct,
        "total_questions": stat.total_questions,
        "accuracy_rate": stat.accuracy_rate
    } for stat in stats]
    return jsonify(stat_list)

# 根據 student_id 查詢特定學生的練習統計
@practice_statistics_bp.route("/practice_statistics/<student_id>", methods=["GET"])
def get_practice_statistic(student_id):
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

# 更新練習統計資料
@practice_statistics_bp.route("/practice_statistics/<student_id>/<unit_id>", methods=["PUT"])
def update_practice_statistic(student_id, unit_id):
    stat = PracticeStatistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Practice statistics not found"}), 404

    data = request.json
    stat.total_correct = data.get("total_correct", stat.total_correct)
    stat.total_questions = data.get("total_questions", stat.total_questions)
    stat.accuracy_rate = data.get("accuracy_rate", stat.accuracy_rate)

    db.session.commit()
    return jsonify({"message": "Practice statistics updated successfully"})

# 刪除練習統計資料
@practice_statistics_bp.route("/practice_statistics/<student_id>/<unit_id>", methods=["DELETE"])
def delete_practice_statistic(student_id, unit_id):
    stat = PracticeStatistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Practice statistics not found"}), 404

    db.session.delete(stat)
    db.session.commit()
    return jsonify({"message": "Practice statistics deleted successfully"})
