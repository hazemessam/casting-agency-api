# Standard library imports
import os
from datetime import date

# Third party imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Table


# Global Variables
DB_URI = os.environ.get('DATABASE_URL', 'splite:///sqlite.db')

db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# Create dummy data for testing
def insert_dummy_data():
    dummy_actors = [
        ('Hazem', '20', 'male'),
        ('Seif', '19', 'male'),
        ('Omer', '20', 'male'),
    ]
    for actor_data in dummy_actors:
        actor_obj = Actor(
            name=actor_data[0],
            age=actor_data[1],
            gender=actor_data[2]
        )
        actor_obj.insert()
    
    dummy_movies = ['Soul', 'Inside Out', 'Joker']
    for movie_data in dummy_movies:
        movie_obj = Movie(title=movie_data)
        movie_obj.insert()
    


Performance = Table(
    'Performance', 
    db.Model.metadata,
    Column('Movie_id', Integer, db.ForeignKey('movies.id')),
    Column('Actor_id', Integer, db.ForeignKey('actors.id'))
)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(32), unique=True, nullable=False)
    release_date = Column(Date, default=date.today)
    actors = db.relationship('Actor', secondary=Performance, backref=db.backref('performances', lazy=True))
    
    def __init__(self, title, release_date=None):
        self.title = title.title()
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return f'Movie(id: {self.id}, title: {self.title}, release_date: {self.release_date})'


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    age = Column(Integer)
    gender = Column(String(32))

    def __init__(self, name, age=None, gender=None):
        self.name = name
        self.age = age
        self.gender = gender
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f'Actor(id: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender})'