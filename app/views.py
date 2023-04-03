from app import app

from flask import request
from datetime import datetime, time

from flask_json import jsonify, json_response

from .models import Institution, CustomUser, Project, db

import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="172.17.0.2",
        database="flask_db",
        user="postgres",
        password="postgres", )
    return conn


@app.route('/institutions', methods=['GET', 'POST'])
def institutions():
    """Get all institutions or create a new one"""
    if request.method == 'GET':
        institutions = Institution.query.all()
        projects = Project.query.all()

        return jsonify([{
            'id': institution.id,
            'name': institution.name,
            'description': institution.description,
            'creation_date': institution.creation_date,
            'projects': [{'project_name': project.name,
                          'responsible': CustomUser.query.filter_by(id=project.responsible).first().get_full_name()}
                         for project in projects]
        } for institution in institutions ])

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
def institution(id: int) -> json_response:
    """Get, update or delete an institution"""
    institution = Institution.query.get(id)
    projects = Project.query.filter_by(institution_id=id).all()


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
            print(request.json)
            name = request.form('name', institution.name)
            description = request.form('description', institution.description)
            address = request.form('address', institution.address)
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
            return json_response(description='Institution not found')

    elif request.method == 'DELETE':
        if institution:
            db.session.delete(institution)
            db.session.commit()
            return json_response(result=True)
        else:
            return json_response(description='Institution not found')

@app.route('/users', methods=['GET', 'POST'])
def users() -> json_response:
    """Get all users or create a new one"""
    if request.method == 'GET':
        users = CustomUser.query.all()

        return jsonify([{
            'id': user.id,
            'first_name': user.first_name,
            'lastnames': user.lastnames,
            'rut': user.rut,
            'birth_date': user.birth_date,
            'position': user.position,
            'age': user.age
        } for user in users])

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
@app.route('/users/<string:rut>', methods=['GET', 'PUT', 'DELETE'])
def user(rut: str) -> json_response:
    """Get, update or delete an user"""
    user = CustomUser.query.filter_by(rut=str(rut)).first()
    projects = Project.query.filter_by(responsible=user.id).all()

    if request.method == 'GET':
        if user:
            return json_response(user={
                'id': user.id,
                'first_name': user.first_name,
                'lastnames': user.lastnames,
                'rut': user.rut,
                'birth_date': user.birth_date,
                'position': user.position,
                'age': user.age,
                'projects': [{'project_name':project.name} for project in projects]

            })
        else:
            return json_response(description='User not found')


@app.route('/projects', methods=['GET', 'POST'])
def projects() -> json_response:
    """Get all projects or create a new one"""
    if request.method == 'GET':
        projects = Project.query.all()

        return jsonify([{
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date,
            'end_date': project.end_date,
            'responsible': project.responsible,
            'institution_id': project.institution_id
        }for project in projects])

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

@app.route('/projects/days_left', methods=['GET'])
def project_days_left() -> json_response:
    """Get all projects with days left to finish"""
    projects = Project.query.all()
    now = datetime.now()
    return jsonify(list({'project_name': project.name,
                         'days_left': str(datetime.combine(project.end_date, time.max) - now) if datetime.combine(project.end_date, time.max) > now else 'finished project'}
                        for project in projects))



@app.route('/institutions/address', methods=['GET'])
def get_google_maps_url() -> json_response:
    """Get all institutions with google maps url"""
    institutions = Institution.query.all()
    return jsonify([{'institution_name': str(institution.name), 'address': f'https://www.google.com/maps/search/?api=1&query={institution.address.replace(" ", "+")}'}
                    for institution in institutions])

