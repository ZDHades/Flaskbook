from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    in_stock = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<{self.name} | {self.price}>" 

    def to_dict(self):
        data = {
            'id' : self.id,
            'name' : self.name,
            'image' : self.image,
            'description' : self.description,
            'price' : self.price
        }

        return data