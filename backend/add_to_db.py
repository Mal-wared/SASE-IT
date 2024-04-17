from sqlalchemy.orm import sessionmaker
from tables import User, Course, Homework, Quiz, engine, Base

# Create a sessionmaker object
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create a new user
new_user = User(username='john_doe', password='password123', email='john@example.com')

# Create a new course
new_course = Course(coursename='CSE 3318', user_id=1)
new_homework = Homework(title='Homework 14.7 Non-Linear Equations', duedate='2021-02-01', course_id=2)
new_quiz = Quiz(title='Quiz 1', date='2021-02-03', course_id=2)

print(new_course.id)



# Add the new user to the session
session.add(new_quiz)

# Commit the session to save the changes to the database
session.commit()

# Close the session
session.close()
