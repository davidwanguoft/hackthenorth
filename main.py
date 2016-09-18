#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,render_template, request, send_file, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction
import requests
from flask_cors import CORS, cross_origin


import json

app = Flask(__name__)
app.config.from_pyfile('config.py')     #set as envar in local windows environment.
CORS(app)

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
    price = db.Column(db.Text)
    desc = db.Column(db.Text)
    imgurl = db.Column(db.Text)
    seller_id = db.Column(db.Integer)

    def __init__(self,name,cat,price,desc,imgurl,seller_id,city='Toronto',country='Canada'):
        self.name = name
        self.category = cat
        self.city = city
        self.country = country
        self.price = price
        self.desc = desc
        self.imgurl = imgurl
        self.seller_id = seller_id


    def dict(self):
        return {
            'name': self.name,
            'cat' : self.category,
            'city': self.city,
            'country' : self.country,
            'price': self.price,
            'desc' : self.desc,
            'imgurl': self.imgurl,
            'seller_id' : self.seller_id
        }





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

    def __repr__(self):
        dat = {
            'name' : self.name,
            'city' : self.city,
            'country' : self.country,
            'phone' : self.phone_num
        }

        return json.dumps(dat)



@app.route('/')
def home():
    return "world. hello."
    return render_template('imageform.html')

@app.route('/api/v1/allprods')
def get_all_prods():

    prods = [p.dict() for p in Product.query.all()]
    for base in prods:
        if base['country'] != 'Canada':
            amount = base['price'][1:]
            if base['country'] == 'UK':
                fc = 'GBP'
            elif base['country'] == 'USA':
                fc = 'USD'
            elif base['country'] == 'JPN':
                fc = 'JPY'

            forex = get_forex(curr1=fc,amt=amount)
            conv = forex['to'][0]['mid']
            conv = "{0:.2f}".format(conv)

            base['convPrice'] = base['price']
            base['price'] = '$' + conv

    return json.dumps(prods)

@app.route('/api/v1/prodinfo')
def get_prods():
    regions = request.args.get('regions').split(',')
    cat = request.args.get('category',default='electronics')

    if cat not in ('electronics','clothing', 'accessories','kitchen'):
        cat = 'electronics'

    for r in regions:
        if r not in ('local','national','international'):
            r.delete

    prods = Product.query.filter(Product.category == cat).all()


    return json.dumps([p.dict() for p in prods])


@app.route('/api/v1/sellinfo/<id>')
def get_seller(id):
    try:
        id = int(id)
    except TypeError:
        return Seller.query.first()

    s = Seller.query.get(id)
    if s == None:
        s = Seller.query.first()

    return str(s)


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
    return resp

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

    id0 = Seller.query[0].id
    id1 = Seller.query[1].id
    with app.test_request_context():
        prods = [
            Product('Soap','kitchen','$5.50','Very good soap',\
                    url_for('static',filename='1.png',_external=True), id0),
            Product('Backpack','accessories','$75.00','School Bag',\
                    url_for('static',filename='2.png',_external=True), id1),
            Product('XPS 13','electronics','$800.34','Sweet laptop',\
                    url_for('static',filename='3.png',_external=True),id0),
            Product('Mac Air', 'electronics', '$900.24', 'Light laptop', \
                    url_for('static',filename='4.png',_external=True),id0),
            Product('IPhone Case', 'accessories', '$14.50','Spigen Iphone Case', \
                    url_for('static',filename='5.png',_external=True), id0),
            Product('Ice Cream Case', 'accessories', '$13.23', 'Ice Cream Iphone Case',\
                    url_for('static',filename='6.png',_external=True), id0),
            Product('USB Hub', 'electronics', '$18.98', 'Belkin USB Hub', \
                    url_for('static',filename='7.png',_external=True), id1),
            Product('Headphones', 'electronics', '$79.99', 'Wireless Stereo Headphones', \
                    url_for('static',filename='8.png',_external=True), id1),
            Product('Fudge', 'kitchen', '£5.40', 'Fudge fudge fudge', \
                    url_for('static',filename='9.png',_external=True), id0, city='London', country='UK'),
            Product('Sweater', 'clothing', '$59.50', 'Flame Sweater', \
                    url_for('static', filename='10.png',_external=True), id0),
            Product('Lava lamp', 'accessories', '$60.12', 'Casual lighting', \
                    url_for('static',filename='11.png',_external=True), id1),
            Product('3D Pen', 'electronics', '$110.31', 'Great for outdoors.',\
                    url_for('static',filename='12.png',_external=True), id0),
            Product('Bento Box', 'kitchen', '¥70.97', 'Bento Lunch Box', \
                    url_for('static',filename='13.png',_external=True), id1, city='Osaka',country='JPN'),
            Product('Corkscrew', 'kitchen', '£20.23', 'LM-G10 Metal Professional Corkscrew', \
                    url_for('static',filename='14.png',_external=True), id1, city='Derbyshire', country='UK')

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
    app.run(host='0.0.0.0',port='80')


