import unittest

from app import app
from app.models import Institution, CustomUser, Project, db


class InstitutionsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.17.0.3/flask_test_db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
        self.institution = Institution(name='Awesome Institution Name', description='This Awesome institution description', address='Awesome Street 948')
        self.another_institution = Institution(name='Another Awesome Institution Name', description='This Another Awesome institution description', address='Another Awesome Street 948')
        self.user = CustomUser(first_name='Awesome', lastnames='User', rut='123456789', birth_date='1990-01-01', position='Awesome Position', age=30)
        self.project = Project(name='Awesome Project Name', description='This Awesome project description', start_date='2020-01-01', end_date='2020-12-31', responsible=1, institution_id=1)
        with app.app_context():
            db.session.add(self.institution)
            db.session.add(self.another_institution)
            db.session.add(self.user)
            db.session.add(self.project)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_institutions(self):
        response = self.app.get('/institutions')
        self.assertEqual(response.status_code, 200)

    def test_create_institution(self):
        data = {
            'name': 'Test Institution NAme',
            'description': 'This is a test institution description',
            'address': '123 Test Street'
        }
        response = self.app.post('/institutions', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], data['name'])

    def test_get_institution(self):
        with app.app_context():
            institution = Institution.query.first()
        response = self.app.get(f'/institutions/{institution.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['institution']['name'], institution.name)

    @unittest.skip('Fails because of DETAIL:  Key (id)=(1) is still referenced from table "project".')
    def test_delete_institution(self):
        response = self.app.delete(f'/institutions/{self.another_institution.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_google_maps_url(self):
        response = self.app.get(f'/institutions/address')
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['address'], 'https://www.google.com/maps/search/?api=1&query=Awesome+Street+948')



class UserTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.17.0.3/flask_test_db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
        self.user = CustomUser(first_name='Awesome', lastnames='User', rut='123456789', birth_date='1990-01-01', position='Awesome Position', age=30)
        with app.app_context():
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        data = {
            'first_name': 'Awesome',
            'lastnames': 'User',
            'rut': '123456789',
            'birth_date': '1990-01-01',
            'position': 'Awesome Position',
            'age': 30
        }
        response = self.app.post('/users', data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        with app.app_context():
            user = CustomUser.query.first()
        response = self.app.get(f'/users/{user.rut}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['first_name'], 'Awesome')

    def test_get_all_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['first_name'], 'Awesome')


class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.17.0.3/flask_test_db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
        self.institution = Institution(name='Awesome Institution Name', description='This Awesome institution description', address='Awesome Street 948')
        self.user = CustomUser(first_name='Awesome', lastnames='User', rut='123456789', birth_date='1990-01-01', position='Awesome Position', age=30)
        self.project = Project(name='Awesome Project Name', description='This Awesome project description', start_date='2020-01-01', end_date='2020-12-31', responsible=1, institution_id=1)
        with app.app_context():
            db.session.add(self.institution)
            db.session.add(self.user)
            db.session.add(self.project)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_projects(self):
        response = self.app.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Awesome Project Name')

    def test_create_project(self):
        data = {
            'name': 'Awesome Project Name',
            'description': 'This Awesome project description',
            'start_date': '2020-01-01',
            'end_date': '2020-12-31',
            'responsible': 1,
            'institution_id': 1
        }
        response = self.app.post('/projects', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], data['name'])

    def test_get_project_days_left(self):
        response = self.app.get(f'/projects/days_left')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['days_left'], 'finished project')

if __name__ == '__main__':
    unittest.main()
