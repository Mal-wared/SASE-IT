from sqlalchemy.orm import sessionmaker
from tables import User, Course, Homework, Quiz, engine, Base

# Create a sessionmaker object
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create a new user
new_user = User(username='john_doe', password='password123', email='john@example.com')
session.add(new_user)
session.commit()

# Create a new course
new_course = Course(coursename='CSE 3318', user_id=new_user.id)
session.add(new_course)
session.commit()

new_homework = Homework(title='Homework 14.8 Super-Linear Equations', duedate='2023-02-01', course_id=new_course.id)
session.add(new_homework)

new_quiz = Quiz(title='Quiz 1', date='2021-02-03', course_id=new_course.id)
session.add(new_quiz)

session.commit()

# Close the session
session.close()
