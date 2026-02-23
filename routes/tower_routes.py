from flask import Blueprint,request,jsonify
from extensions import db
from models.tower import Tower
from utils.decorators import admin_required
from flask_jwt_extended import jwt_required

tower_bp = Blueprint('tower',__name__)

#creating tower : admin only
@tower_bp.route("/add-tower",methods=['POST'])
@admin_required
def create_tower():
	data = request.get_json()
	new_tower = Tower(
		name=data['name'],
		total_units=data['total_units']
	)
	db.session.add(new_tower)
	db.session.commit()
	return jsonify({'message':f"Tower : {new_tower.name} created successfully"}),201

#for viewing towers
@tower_bp.route('/',methods=['GET'])
@jwt_required()
def view_towers():
	towers=Tower.query.all()
	result = [
		{
			'id':tower.id,
			'name':tower.name,
			'total_units':tower.total_units
		}
		for tower in towers
	]
	return jsonify(result)