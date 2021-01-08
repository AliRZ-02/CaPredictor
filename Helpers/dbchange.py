# Name: Ali Raza Zaidi
# Date: Jan 8 2021
# Purpose: Clear database during testing

# Import Statements
from app import db

# While working on the project, whenever I needed to clean the database, I would simply run this file

db.drop_all()
db.create_all()