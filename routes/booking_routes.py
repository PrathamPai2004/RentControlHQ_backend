from flask import Blueprint,request,jsonify
from extensions import db
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.booking import Booking
from utils.decorators import admin_required
from models.unit import Unit
from models.lease import Lease
booking_bp = Blueprint('booking',__name__)
from datetime import date

#add booking : user only
@booking_bp.route('/add-booking',methods=['POST'])
@jwt_required()
def book_units():
	data = request.get_json()
	user_id = get_jwt_identity()

	unit = Unit.query.get(data['unit_id'])

	if not unit:
		return jsonify({"error":"Unit not found"}),404
	if unit.status=="booked":
		return jsonify({"error":"Unit is already occupied"}),400
	
	existing_booking = Booking.query.filter_by(
		unit_id=unit.id,
		status="pending"
	).first()
	if existing_booking:
		return jsonify({'error':'unit number already booked by other party'}),400
	
	new_booking=Booking(
			user_id=int(user_id),
			unit_id=data['unit_id']
	)
	db.session.add(new_booking)
	db.session.commit()

	return jsonify({
		"message":f"unit {new_booking.unit_id} boooked success",
		"booking_id":new_booking.id
	}),201

#view-boooking (admin: all bookings)
@booking_bp.route('/get-bookings',methods=['GET'])
@admin_required
def view_bookings():
	bookings = Booking.query.all()

	return(jsonify([
		{
			'id':booking.id,
			'user_id':booking.user_id,
			'unit_id':booking.unit_id,
			'status':booking.status
		}
		for booking in bookings
	]))

# view my bookings (user: own bookings only)
@booking_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def my_bookings():
	user_id = get_jwt_identity()
	bookings = Booking.query.filter_by(user_id=int(user_id)).all()
	return jsonify([
		{
			'id': b.id,
			'unit_id': b.unit_id,
			'status': b.status
		}
		for b in bookings
	])



@booking_bp.route('/<int:id>/approve',methods=['PUT'])
@admin_required
def approve_booking(id):
	booking = Booking.query.get(id)
	if not booking:
		return jsonify({"error":"Booking not found"}),404
	if booking.status!="pending":
		return jsonify({"error":"Booking already processed"}),400
	
	unit = Unit.query.get(booking.unit_id)

	if unit.status!='available':
		return jsonify({"error":"Unit not available - For  booking"}),400
	
	booking.status="approved"

	unit.status="booked"

	lease =  Lease(
		booking_id=id,
		user_id=booking.user_id,
		unit_id=booking.unit_id,
		start_date=date.today()
	)
	db.session.add(lease)
	db.session.commit()

	return jsonify({"message":"Booking approved  and lease created"}),200

@booking_bp.route('/<int:id>/reject-booking',methods=['PUT'])
@admin_required
def reject_booking(id):
	booking = Booking.query.get(id)

	if not booking:
		return jsonify({"error":"booking not found on this id"}),404
	if booking.status!="pending":
		return jsonify({"error":"Booking already processed"}),400
	booking.status="rejected"
	db.session.commit()

	return jsonify({"message":"Booking rejected successfully"}),200