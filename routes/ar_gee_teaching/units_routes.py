from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Units
from models import db

units_bp = Blueprint('units_bp', __name__)

# 取得所有單元資料
@units_bp.route("/units", methods=["GET"])
def get_units():
    units = Units.query.all()
    units_data = [
        {
            "unit_id": unit.unit_id,
            "unit_name": unit.unit_name,
            "video_code": unit.video_code
        }
        for unit in units
    ]
    return jsonify(units_data)

# 取得單一單元資料
@units_bp.route("/units/<unit_id>", methods=["GET"])
def get_unit(unit_id):
    unit = Units.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404
    unit_data = {
        "unit_id": unit.unit_id,
        "unit_name": unit.unit_name,
        "video_code": unit.video_code
    }
    return jsonify(unit_data)

# 新增單元資料
@units_bp.route("/units", methods=["POST"])
def create_unit():
    data = request.json
    unit = Units(
        unit_id=data.get("unit_id"),
        unit_name=data.get("unit_name"),
        video_code=data.get("video_code")
    )
    db.session.add(unit)
    db.session.commit()
    return jsonify({"message": "Unit created successfully"}), 201

# 更新單元資料
@units_bp.route("/units/<unit_id>", methods=["PUT"])
def update_unit(unit_id):
    unit = Units.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404

    data = request.json
    unit.unit_name = data.get("unit_name", unit.unit_name)
    unit.video_code = data.get("video_code", unit.video_code)

    db.session.commit()
    return jsonify({"message": "Unit updated successfully"})

# 刪除單元資料
@units_bp.route("/units/<unit_id>", methods=["DELETE"])
def delete_unit(unit_id):
    unit = Units.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404

    db.session.delete(unit)
    db.session.commit()
    return jsonify({"message": "Unit deleted successfully"})
