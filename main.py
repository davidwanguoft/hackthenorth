from flask import Flask,render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction
import requests
#from database import db, Product, Seller

import json

app = Flask(__name__)
app.config.from_pyfile('config.py')     #set as envar in local windows environment.
#db.init_app(app)
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

class Product(db.Model):
    #__tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    price = db.Column(db.Float)
    desc = db.Column(db.Text)
    imgurl = db.Column(db.Text)
    seller_id = db.Column(db.Integer)

    def __init__(self,name,cat,city,country,price,desc,imgurl,seller_id):
        self.name = name
        self.category = cat
        self.city = city
        self.country = country
        self.price = price
        self.desc = desc
        self.imgurl = imgurl
        self.seller_id = seller_id


class Seller(db.Model):
    #__tablename__ = 'seller'

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




@app.route('/')
def home():
    return render_template('imageform.html')

@app.route('/imform',methods=['POST'])
def upload():
    if 'pricetag' not in request.files:
        return redirect(url_for('home'))

    f = request.files['pricetag']
    f.save('/tmp/htn/yes.jpg')
    return send_file('/tmp/htn/yes.jpg', mimetype='image/jpeg')


def get_forex(curr1='USD', curr2='CAD', amt='50'):

    url = 'https://xecdapi.xe.com/v1/'

    r = requests.get('https://xecdapi.xe.com/v1/convert_from.json/?from=' + curr1 + '&to=' + curr2 +\
            '&amount=' + amt,auth=('hackthenorth041','Waterloo22027'))

    resp = json.loads(r.text)
    print(resp)


def create_db():
    db.drop_all()

    db.create_all()


    sellers =[
        Seller('Eric','Toronto','Canada',4166471010),
        Seller('Alice','Missisauga', 'Canada', 6479059483),
        Seller('Sam','Waterloo','Canada',5194049382),
        Seller('Hoi Lo', 'Hong Kong', 'China', 8521029383),]

    def callback(session):
        for s in sellers:
            session.add(s)

    run_transaction(sessionmaker, callback)

    prods = [
        Product('Soap','kitchen','Toronto','Canada',45.50,'Very good soap',\
                'http://www.healthyblackwoman.com/wp-content/uploads/2015/01/download19.jpg', 0),
        Product('Backpack','accessories','Toronto','Canada',75.00,'School Bag',\
                'http://targus.com/content/images/thumbs/0003402_17-groove-backpack.jpeg', 1)
    ]

    def callback(session):
        for p in prods:
            session.add(p)

    run_transaction(sessionmaker, callback)


if __name__ == "__main__":

    print(Seller.query.all())
    print(Product.query.all())
    ids = Product.query[1].seller_id
    print(ids)
    print(Seller.query[0].id)
    print(Seller.query[1].id)
    print(Product.query[0].id)
    app.run(debug=True)


