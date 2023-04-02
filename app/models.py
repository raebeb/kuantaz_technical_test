from app import app

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.17.0.2/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
