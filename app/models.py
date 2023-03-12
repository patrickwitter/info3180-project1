from . import db


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    property_type = db.Column(db.String(10))
    location = db.Column(db.String(256))
    price = db.Column(db.String(15))
    description = db.Column(db.Text())
    bedrooms = db.Column(db.String(3))
    bathrooms = db.Column(db.String(3))
    photo_filename = db.Column(db.String(256))


    def __init__(self, title, prop_type, location, price, description, bedrooms, bathrooms, photo_filename):
        self.title = title
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.location = location
        self.price = price
        self.property_type = prop_type
        self.description = description
        self.photo_filename = photo_filename


    def __repr__(self):
        return '<Property %r>' % (self.title)