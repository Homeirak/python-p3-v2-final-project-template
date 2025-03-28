# lib/cli.py

from helpers import (
    exit_program,
    student_menu,
    # course_menu
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            student_menu()
        # elif choice == "2":
        #     course_menu()
        else:
            print("Invalid choice. Please try again.\n")

def menu():
    print("\nWelcome to BinaryBoost School CLI!")
    print("Please select an option:")
    print("1. Student Management")
    print("2. Course Management")
    print("0. Exit")

if __name__ == "__main__":
    main()