from extensions import db
from flask import request,Blueprint,jsonify
from models.lease import Lease
from utils.decorators import admin_required

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
				'start_date':l.start_date,
				'end_date':l.end_date
			}
			for l in leases
		]
	)