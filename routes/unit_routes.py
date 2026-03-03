from flask import Blueprint,request,jsonify
from extensions import db
from models.unit import Unit
from utils.decorators import admin_required
from flask_jwt_extended import jwt_required
from models.unit import Unit
from models.tower import Tower

unit_bp = Blueprint('unit',__name__)

@unit_bp.route('/add-unit',methods=['POST'])
@admin_required
def create_unit():
	data = request.get_json()

	#validate tower exists
	tower = Tower.query.get(data['tower_id'])
	if not tower:
		return jsonify({'error':'Tower not found'}),404
	if data['unit_number']> tower.total_units:
		return jsonify({
    "error": f"Unit number {data['unit_number']} exceeds the maximum units ({tower.total_units}) in Tower {tower.id}"
}), 400
	new_unit=Unit(
		tower_id=data['tower_id'],
		unit_number=data['unit_number'],
		rent=data['rent']
	)
	db.session.add(new_unit)
	db.session.commit()

	return jsonify({
		"message":f"{new_unit} created successfully",
		"status of unit":new_unit.status
	}),201

#viewing units
@unit_bp.route('/get-units/<int:tower_id>',methods=['GET'])
@jwt_required()
def get_units(tower_id):
	show_all = request.args.get('all', 'false').lower() == 'true'

	if show_all:
		units = Unit.query.filter_by(tower_id=tower_id).all()
	else:
		units = Unit.query.filter_by(tower_id=tower_id, status="available").all()

	return jsonify([
		{
			'unit id': unit.id,
			'tower_id': unit.tower_id,
			'unit_number': unit.unit_number,
			'rent': unit.rent,
			'status': unit.status
		}
		for unit in units
	])