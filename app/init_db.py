import psycopg2

conn = psycopg2.connect(
        host="172.17.0.2",
        database="flask_db",
        user="postgres",
        password="postgres",)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS institution;')
cur.execute('DROP TABLE IF EXISTS project;')
cur.execute('DROP TABLE IF EXISTS custom_user;')

cur.execute('CREATE TABLE institution (id serial PRIMARY KEY,'
                                     'name varchar (150) NOT NULL,'
                                     'description varchar (150) NOT NULL,'
                                     'creation_date date DEFAULT CURRENT_TIMESTAMP);'
                                     )

cur.execute('CREATE TABLE custom_user (id serial PRIMARY KEY,'
                                        'first_name varchar (150) NOT NULL,'
                                        'lastnames varchar (150) NOT NULL,'
                                        'rut varchar (150) NOT NULL,'
                                        'birth_date date NOT NULL,'
                                        'position varchar (150) NOT NULL,'
                                        'age integer NOT NULL);'
                                        )

cur.execute('CREATE TABLE project (id serial PRIMARY KEY,'
                                    'name varchar (150) NOT NULL,'
                                    'description varchar (150) NOT NULL,'
                                    'start_date date NOT NULL,'
                                    'end_date date NOT NULL,'
                                    'responsible integer NOT NULL,'
                                    'institution_id integer NOT NULL);'
                                    )

cur.execute('ALTER TABLE project ADD CONSTRAINT fk_institution FOREIGN KEY (institution_id) REFERENCES institution (id);')
cur.execute('ALTER TABLE project ADD CONSTRAINT fk_responsible FOREIGN KEY (responsible) REFERENCES custom_user (id);')

conn.commit()

cur.close()
conn.close()