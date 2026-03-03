from extensions import db
from flask import request,Blueprint,jsonify
from models.lease import Lease
from utils.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

lease_bp = Blueprint("leases",__name__)

@lease_bp.route('/get-leases',methods=['GET'])
@admin_required
def get_leases():
	leases = Lease.query.all()

	return jsonify(
		[
			{
				'lease_id':l.id,
				'booking_id':l.booking_id,
				'user_id':l.user_id,
				'start_date':str(l.start_date),
				'end_date':str(l.end_date) if l.end_date else None
			}
			for l in leases
		]
	)

# user: view own lease only
@lease_bp.route('/my-lease', methods=['GET'])
@jwt_required()
def my_lease():
	user_id = get_jwt_identity()
	leases = Lease.query.filter_by(user_id=int(user_id)).all()
	return jsonify([
		{
			'lease_id': l.id,
			'booking_id': l.booking_id,
			'start_date': str(l.start_date),
			'end_date': str(l.end_date) if l.end_date else None
		}
		for l in leases
	])
