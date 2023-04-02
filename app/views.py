from app import app

import psycopg2
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_json import FlaskJSON, jsonify,  JsonError, json_response



import os
import psycopg2
from flask import Flask, render_template


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.17.0.2/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Models
class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    address = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Institution(id={self.id}, name='{self.name}', description='{self.description}', creation_date='{self.creation_date}')"


def get_db_connection():
    conn = psycopg2.connect(
        host="172.17.0.2",
        database="flask_db",
        user="postgres",
        password="postgres", )
    return conn

@app.route('/test')
def home():
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute('SELECT * FROM institution;')
   inst = cur.fetchall()
   cur.close()
   conn.close()
   return render_template('index.html', inst=inst)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/institutions', methods=['GET', 'POST'])
def institutions():
    if request.method == 'GET':
        institutions = Institution.query.all()
        institutions_list = []

        for institution in institutions:
            institution_dict = {
                'id': institution.id,
                'name': institution.name,
                'description': institution.description,
                'creation_date': institution.creation_date
            }
            institutions_list.append(institution_dict)

        return jsonify(institutions_list)

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        address = request.form['address']
        institution = Institution(name=name, description=description, address=address)
        db.session.add(institution)
        db.session.commit()

        institution_dict = {
            'id': institution.id,
            'name': institution.name,
            'description': institution.description,
            'creation_date': institution.creation_date
        }

        return jsonify(institution_dict)



@app.route('/institutions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def institution(id):
    institution = Institution.query.get(id)
    print(f'INSTITUTION->{institution}')

    if request.method == 'GET':
        if institution:
            return json_response(institution={
                'id': institution.id,
                'name': institution.name,
                'description': institution.description,
            })
        else:
            return json_response(description='Institution not found')

    elif request.method == 'PUT':
        if institution:
            print('PUT')
            print(request.json)
            name = request.form('name', institution.name)
            description = request.form('description', institution.description)
            address = request.form('address', institution.address)
            print(f'NAME->{name} DESCRIPTION->{description}')
            institution.name = name
            institution.description = description
            institution.address = address
            db.session.commit()
            return json_response(institution={
                'id': institution.id,
                'name': institution.name,
                'description': institution.description,
            })
        else:
            print('PUT ELSE')
            return json_response(description='Institution not found')

    elif request.method == 'DELETE':
        if institution:
            db.session.delete(institution)
            db.session.commit()
            return json_response(result=True)
        else:
            return json_response(description='Institution not found')
