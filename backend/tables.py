from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os

# Specify the directory where you want to store the SQLite database file
directory = 'backend'

# Specify the filename for the SQLite database
db_filename = 'User.db'

# Combine the directory and filename to create the full path
db_path = f'{os.path.join(os.getcwd(), directory, db_filename)}'

print(f'DB Path is: {db_path}')

# Create an engine object to connect to the SQLite database
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Define a base class for your database models
Base = declarative_base()

# Define your data model
class User(Base):
    __tablename__ = 'users'

    id          = Column(Integer, primary_key = True)
    username    = Column(String)
    password    = Column(String)
    email       = Column(String)
    courses     = relationship("Course", backref="user")

class Course(Base):
    __tablename__ = 'courses'

    id          = Column(Integer, primary_key = True)
    coursename  = Column(String)
    user_id     = Column(Integer, ForeignKey('users.id'))

class Homework(Base):
    __tablename__= 'homeworks'

    id          = Column(Integer, primary_key = True)
    title       = Column(String)
    duedate     = Column(String)
    course_id   = Column(Integer, ForeignKey('courses.id'))

class Quiz(Base):
    __tablename__= 'quizzes'

    id          = Column(Integer, primary_key = True)
    title       = Column(String)
    date        = Column(String)
    course_id   = Column(Integer, ForeignKey('courses.id'))

# Create the tables in the database
Base.metadata.create_all(engine)

