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
#TODO: move this to a models.py file
class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    address = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Institution(id={self.id}, name='{self.name}', description='{self.description}', creation_date='{self.creation_date}')"

class CustomUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    lastnames = db.Column(db.String(200))
    rut = db.Column(db.String(200))
    birth_date = db.Column(db.DateTime)
    position = db.Column(db.String(200))
    age = db.Column(db.Integer)

    def get_full_name(self):
        return f"{self.first_name} {self.lastnames}"

    def __repr__(self):
        return f"CustomUser(id={self.id}, first_name='{self.first_name}', lastnames='{self.lastnames}', rut='{self.rut}', birth_date='{self.birth_date}', position='{self.position}', age='{self.age}')"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    responsible = db.Column(db.Integer, db.ForeignKey('custom_user.id'))
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}', description='{self.description}', start_date='{self.start_date}', end_date='{self.end_date}', responsible='{self.responsible}', institution_id='{self.institution_id}')"


def get_db_connection():
    conn = psycopg2.connect(
        host="172.17.0.2",
        database="flask_db",
        user="postgres",
        password="postgres", )
    return conn


@app.route('/institutions', methods=['GET', 'POST'])
def institutions():
    if request.method == 'GET':
        institutions = Institution.query.all()
        projects = Project.query.all()
        institutions_list = []

        for institution in institutions:
            institution_dict = {
                'id': institution.id,
                'name': institution.name,
                'description': institution.description,
                'creation_date': institution.creation_date,
                'projects': [{'project_name': project.name,
                'responsible': CustomUser.query.filter_by(id=project.responsible).first().get_full_name()}
                for project in projects]
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
    projects = Project.query.filter_by(institution_id=id).all()

    print(f'INSTITUTION->{institution}')

    if request.method == 'GET':
        if institution:
            return json_response(institution={
                'id': institution.id,
                'name': institution.name,
                'description': institution.description,
                'projects': [{'project_name':project.name, 'responsible': CustomUser.query.filter_by(id=project.responsible).first().get_full_name() } for project in projects]

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

@app.route('/users', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        users = CustomUser.query.all()
        users_list = []

        for user in users:
            user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'lastnames': user.lastnames,
                'rut': user.rut,
                'birth_date': user.birth_date,
                'position': user.position,
                'age': user.age
            }
            users_list.append(user_dict)

        return jsonify(users_list)

    elif request.method == 'POST':
        first_name = request.form['first_name']
        lastnames = request.form['lastnames']
        rut = request.form['rut']
        birth_date = request.form['birth_date']
        position = request.form['position']
        age = request.form['age']
        user = CustomUser(first_name=first_name, lastnames=lastnames, rut=rut, birth_date=birth_date, position=position, age=age)
        db.session.add(user)
        db.session.commit()

        user_dict = {
            'id': user.id,
            'first_name': user.first_name,
            'lastnames': user.lastnames,
            'rut': user.rut,
            'birth_date': user.birth_date,
            'position': user.position,
            'age': user.age
        }

        return jsonify(user_dict)

@app.route('/projects', methods=['GET', 'POST'])
def project():
    if request.method == 'GET':
        projects = Project.query.all()
        projects_list = []

        for project in projects:
            project_dict = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'responsible': project.responsible,
                'institution_id': project.institution_id
            }
            projects_list.append(project_dict)

        return jsonify(projects_list)
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        responsible = request.form['responsible']
        institution_id = request.form['institution_id']
        project = Project(name=name, description=description, start_date=start_date, end_date=end_date, responsible=responsible, institution_id=institution_id)
        db.session.add(project)
        db.session.commit()

        project_dict = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date,
            'end_date': project.end_date,
            'responsible': project.responsible,
            'institution_id': project.institution_id
        }

        return jsonify(project_dict)