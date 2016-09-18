from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    price = db.Column(db.Float)
    desc = db.Column(db.Text)
    imgurl = db.Column(db.Text)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))
    seller = db.relationship('Seller',backref=db.backref('listings', lazy='dynamic'))

    def __init__(self,name,cat,city,country,price,desc,imgurl,seller_id):
        self.name = name
        self.category = cat
        self.city = city
        self.country = country
        self.price = price
        self.desc = desc
        self.imgur = imgurl
        self.seller_id = seller_id

class Seller(db.Model):
    __tablename__ = 'seller'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    phone_num = db.Column(db.Integer)

    def __init__(self, name, city, country, phone_num):
        self.name = name
        self.city = city
        self.country = country
        self.phone_num = phone_num



