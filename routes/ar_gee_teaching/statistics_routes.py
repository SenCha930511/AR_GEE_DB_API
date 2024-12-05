from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Statistics
from models import db

# 定義 Blueprint
statistics_bp = Blueprint("statistics_bp", __name__)

# 新增統計資料
@statistics_bp.route("/statistics", methods=["POST"])
def add_statistic():
    data = request.json
    new_stat = Statistics(
        student_id=data["student_id"],
        unit_id=data["unit_id"],
        total_correct=data["total_correct"],
        total_questions=data["total_questions"],
        accuracy_rate=data["accuracy_rate"]
    )
    db.session.add(new_stat)
    db.session.commit()
    return jsonify({"message": "Statistic added successfully"}), 201

# 查詢所有統計資料
@statistics_bp.route("/statistics", methods=["GET"])
def get_statistics():
    stats = Statistics.query.all()
    stat_list = [{
        "student_id": stat.student_id,
        "unit_id": stat.unit_id,
        "total_correct": stat.total_correct,
        "total_questions": stat.total_questions,
        "accuracy_rate": stat.accuracy_rate
    } for stat in stats]
    return jsonify(stat_list)

# 根據 student_id 和 unit_id 查詢特定統計資料
@statistics_bp.route("/statistics/<student_id>/<unit_id>", methods=["GET"])
def get_statistic(student_id, unit_id):
    stat = Statistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
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

# 更新統計資料
@statistics_bp.route("/statistics/<student_id>/<unit_id>", methods=["PUT"])
def update_statistic(student_id, unit_id):
    stat = Statistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Statistic not found"}), 404

    data = request.json
    stat.total_correct = data.get("total_correct", stat.total_correct)
    stat.total_questions = data.get("total_questions", stat.total_questions)
    stat.accuracy_rate = data.get("accuracy_rate", stat.accuracy_rate)

    db.session.commit()
    return jsonify({"message": "Statistic updated successfully"})

# 刪除統計資料
@statistics_bp.route("/statistics/<student_id>/<unit_id>", methods=["DELETE"])
def delete_statistic(student_id, unit_id):
    stat = Statistics.query.filter_by(student_id=student_id, unit_id=unit_id).first()
    if not stat:
        return jsonify({"error": "Statistic not found"}), 404

    db.session.delete(stat)
    db.session.commit()
    return jsonify({"message": "Statistic deleted successfully"})
