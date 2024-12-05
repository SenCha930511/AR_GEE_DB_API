from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeUnits
from models import db

# 定義 Blueprint
practice_unit_bp = Blueprint("practice_unit_bp", __name__)

# 新增練習單元資料
@practice_unit_bp.route("/practice_units", methods=["POST"])
def add_practice_unit():
    data = request.json
    new_unit = PracticeUnits(
        unit_id=data["unit_id"],
        unit_name=data["unit_name"],
        video_code=data["video_code"]
    )
    db.session.add(new_unit)
    db.session.commit()
    return jsonify({"message": "Practice unit added successfully"}), 201

# 查詢所有練習單元資料
@practice_unit_bp.route("/practice_units", methods=["GET"])
def get_practice_units():
    units = PracticeUnits.query.all()
    unit_list = [{
        "unit_id": unit.unit_id,
        "unit_name": unit.unit_name,
        "video_code": unit.video_code
    } for unit in units]
    return jsonify(unit_list)

# 根據 unit_id 查詢特定練習單元
@practice_unit_bp.route("/practice_units/<unit_id>", methods=["GET"])
def get_practice_unit(unit_id):
    unit = PracticeUnits.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Practice unit not found"}), 404
    unit_data = {
        "unit_id": unit.unit_id,
        "unit_name": unit.unit_name,
        "video_code": unit.video_code
    }
    return jsonify(unit_data)

# 更新練習單元資料
@practice_unit_bp.route("/practice_units/<unit_id>", methods=["PUT"])
def update_practice_unit(unit_id):
    unit = PracticeUnits.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Practice unit not found"}), 404

    data = request.json
    unit.unit_name = data.get("unit_name", unit.unit_name)
    unit.video_code = data.get("video_code", unit.video_code)

    db.session.commit()
    return jsonify({"message": "Practice unit updated successfully"})

# 刪除練習單元資料
@practice_unit_bp.route("/practice_units/<unit_id>", methods=["DELETE"])
def delete_practice_unit(unit_id):
    unit = PracticeUnits.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Practice unit not found"}), 404

    db.session.delete(unit)
    db.session.commit()
    return jsonify({"message": "Practice unit deleted successfully"})
