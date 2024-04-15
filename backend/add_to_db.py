from sqlalchemy.orm import sessionmaker
from tables import User, Course, Homework, Quiz, engine, Base

# Create a sessionmaker object
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create a new user
new_user = User(username='john_doe', password='password123', email='john@example.com')

# Add the new user to the session
session.add(new_user)

# Commit the session to save the changes to the database
session.commit()

# Close the session
session.close()
