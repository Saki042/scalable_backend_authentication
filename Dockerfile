# Using lightweight alpine image
FROM python:3.10.12

# Installing packages
RUN apt-get update && apt-get install -y sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN pip install --no-cache-dir pipenv
RUN pip install flask
RUN pip install flask-sqlalchemy


# Defining working directory and adding source code
WORKDIR /app
COPY . /app

ENV FLASK_APP=./booksappcode/index.py

# Install API dependencies
RUN pipenv install --system --deploy

# Start app
EXPOSE 5000
#CMD ["pipenv", "run", "flask", "--debug", "run", "-h 0.0.0.0"]
ENTRYPOINT [ "/app/bootstrap.sh"]