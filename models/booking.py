from extensions import db
from datetime import date

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")
    booking_date = db.Column(db.Date, default=date.today)
