from extensions import db

class Lease(db.Model):
    __tablename__ = "leases"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), unique=True, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    unit_id=db.Column(db.Integer,db.ForeignKey("units.id"))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
