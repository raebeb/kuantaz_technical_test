#FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
#RUN apk --update add bash nano
#ENV STATIC_URL /static
#ENV STATIC_PATH /var/www/app/static
#COPY ./requirements.txt /var/www/requirements.txt
#RUN pip install -r /var/www/requirements.txt
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk --update add bash nano

# Install PostgreSQL and psycopg2
RUN apk add --no-cache postgresql-libs postgresql-dev gcc python3-dev musl-dev \
    && pip install psycopg2

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

# Copy the application code
COPY ./app /app

# Install application dependencies
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

# Set the database URL environment variable
ENV DATABASE_URL postgres://user:password@postgres/db_name

# Expose the port that the application will listen on
EXPOSE 80

# Start the application
CMD ["uwsgi", "--http-socket", "0.0.0.0:80", "--master", "--wsgi-file", "/app/main.py", "--callable", "app", "--processes", "4", "--threads", "2"]
