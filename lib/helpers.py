# lib/helpers.py

# def helper_1():
#     print("Performing useful function#1.")


# def exit_program():
#     print("Goodbye!")
#     exit()

from models.Student import Student
from models.Course import Course

def exit_program():
    print("Goodbye!")
    exit()

def student_menu():
    while True:
        print("\n-- Student Management --")
        print("1. Create student")
        print("2. Delete student")
        print("3. Update student")
        print("4. View all students")
        print("5. Find student by email")
        print("6. View students by course")
        print("0. Return to main menu")

        choice = input("> ")
        if choice == "0":
            break
        elif choice == "1":
            create_student()
        elif choice == "2":
            delete_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            display_students()
        elif choice == "5":
            find_student_by_email()
        elif choice == "6":
            find_students_by_course()
        else:
            print("Invalid choice. Try again.\n")

def create_student():
    try:
        first = input("First name: ")
        last = input("Last name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        gpa = float(input("GPA (0.0 - 4.0): "))
        course_id = int(input("Course ID: "))

        if not Course.find_by_id(course_id):
            print("Warning: No course found with that ID. Please create the course first or check the ID.")
            return

        Student.create(first, last, phone, email, gpa, course_id)
        print(f"Student '{first} {last}' added successfully.")
    except Exception as e:
        print(f"Error: {e}")

def delete_student():
    try:
        id = int(input("Enter student ID to delete: "))
        student = Student.find_by_id(id)
        if student:
            student.delete()
            print("Student deleted.")
        else:
            print("Student not found.")
    except Exception as e:
        print(f"Error: {e}")

def update_student():
    try:
        id = int(input("Enter student ID to update: "))
        student = Student.find_by_id(id)
        if student:
            print("Leave blank to keep current value.")
            first = input(f"First ({student.first}): ") or student.first
            last = input(f"Last ({student.last}): ") or student.last
            phone = input(f"Phone ({student.phone}): ") or student.phone
            email = input(f"Email ({student.email}): ") or student.email
            gpa = input(f"GPA ({student.gpa}): ") or student.gpa
            course_id_input = input(f"Course ID ({student.course_id}): ") or str(student.course_id)
            course_id = int(course_id_input)

            if not Course.find_by_id(course_id):
                print("Warning: No course found with that ID. Please create the course first or check the ID.")
                return

            student.first = first
            student.last = last
            student.phone = phone
            student.email = email
            student.gpa = float(gpa)
            student.course_id = course_id
            student.update()
            print("Student updated.")
        else:
            print("Student not found.")
    except Exception as e:
        print(f"Error: {e}")

def display_students():
    students = Student.get_all()
    if students:
        print("\nAll Students:")
        for s in students:
            print(f"{s.id}. {s.first} {s.last} | GPA: {s.gpa} | Course ID: {s.course_id}")
    else:
        print("No students found.")

def find_student_by_email():
    email = input("Enter student email: ")
    student = Student.find_by_email(email)
    if student:
        print(f"Found: {student.first} {student.last} | Phone: {student.phone} | GPA: {student.gpa}")
    else:
        print("Student not found.")

def find_students_by_course():
    try:
        course_id = int(input("Enter Course ID: "))
        students = Student.find_by_class_id(course_id)
        if students:
            print(f"Students in Course {course_id}:")
            for s in students:
                print(f"{s.id}. {s.first} {s.last} | GPA: {s.gpa}")
        else:
            print("No students found for that course.")
    except Exception as e:
        print(f"Error: {e}")
