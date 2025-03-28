# lib/setup.py

from models.Course import Course
from models.Student import Student

def setup_database():
    Course.create_table()
    Student.create_table()

    # Optional: clear all existing data (uncomment if needed)
    # Course.drop_table()
    # Student.drop_table()
    # Course.create_table()
    # Student.create_table()

    # Seed a course
    if not Course.find_by_name("Intro to Python"):
        Course.create("Ms. Ada Lovelace", "Intro to Python", "Spring 2025")
        print("Course added successfully.")
    else:
        print("Course already exists.")

if __name__ == "__main__":
    setup_database()