from extensions import db

class Unit(db.Model):
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    tower_id = db.Column(db.Integer, db.ForeignKey("towers.id"), nullable=False)
    unit_number = db.Column(db.String(20), nullable=False)
    rent = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(20), default="available")

    # bookings = db.relationship("Booking", backref="unit", cascade="all, delete")
