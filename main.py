from auth import login
from auth import create_account
from manager import StudentManager, COURSES, SUBJECTS
import pwinput

def auth_menu():
    print("\n===== Student Management System =====")
    print("1. Login")
    print("2. Create Account")
    print("3. Exit")
    print("=====================================")

def main_menu(username):
    print(f"\n===== Main Menu [{username}] =====")
    print("1. Add Student")
    print("2. Add Marks")
    print("3. View All Students")
    print("4. Search Student by ID")
    print("5. View Report Card")
    print("6. Filter By Course")
    print("7. Delete Student")
    print("8. Logout")
    print("=====================================")

def pick_from_list(options, label):
    print(f'\nAvailable {label}s:')
    for i, option in enumerate(options, start=1):
        print(f' {i}. {option}')
    while True:
        try:
            choice = int(input(f'Select {label} (1-{len(options)}): '))
            if 1 <= choice <= len(options):
                print(f"\nSelected: {options[choice - 1]}\n")
                return options[choice - 1]
            print(f'Enter a number between 1 and {len(options)}.')
        except ValueError:
            print('Enter a number.')

def get_valid_age():
    while True:
        try:
            age = int(input('Age: '))
            if age > 0:
                return age
            print('Age must be greater than zero.')
        except ValueError:
            print('Age must be a whole number.')

def get_valid_mark(subject):
    while True:
        try:
            mark = int(input(f'Mark for {subject} (0-100): '))
            if 0 <= mark <= 100:
                return mark
            print('Mark must be between 0 and 100.')
        except ValueError:
            print('Enter a whole number.')

def handle_add_student(manager):
    name = input('Name: ').strip()
    age = get_valid_age()
    course = pick_from_list(COURSES, 'course')
    student = manager.add_student(name, age, course)
    manager.display_student_card(student)
    manager.save_to_file()

def handle_add_marks(manager):
    student_id = input('Student ID: ').strip()
    student = manager.find_by_id(student_id)
    if student is None:
        print("Student not found.")
        return
    
    print(f"Student found: {student.name}")

    while True:
        print("\nAvailable Subjects:")
        for i, subject in enumerate(SUBJECTS, start=1):
            print(f" {i}. {subject}")

        choice = input("Select Subject (1-9, or 0 to finish): ").strip()

        if choice == "0":
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(SUBJECTS):
                subject = SUBJECTS[index]
                print(f"Selected: {subject}")
                mark = get_valid_mark(subject)
                manager.add_marks(student_id, subject, mark)
                print("Mark added.")
            else:
                print("Invalid subject number.")
        except ValueError:
            print("Enter a valid number.")

    manager.save_to_file()
    print(f"Marks saved for {student_id}")

def handle_delete(manager):
    student_id = input('Student ID: ').strip()
    student = manager.find_by_id(student_id)
    if student is None:
        print("Student not found.")
        return
    print(f"Student found: {student.name}")
    select = input("Are you sure? (yes/no): ")

    if select == 'yes':
        manager.delete_student(student_id)
    elif select == 'no':
        print("No student deletion!")
    else:
        print("Invalid choice")
     

def main():
    
    current_user = None
    while True:
        if current_user is None:
            auth_menu()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                username = input("Username: ").strip()
                password = pwinput.pwinput(prompt= "Password: ".strip(), mask = '*')
                if login(username, password):
                    print(f"Welcome, {username}! Data loaded successfully.")
                    current_user = username
                    manager = StudentManager()

                else:
                    print("Invalid username or password.")
                    
            elif choice == "2":
                print("\n--- Create Account ---")
                username = input("Choose a username: ")
                password = pwinput.pwinput(prompt= "Choose a password (min 6 characters): ".strip(), mask = '*')
                
                try:
                    create_account(username, password)
                    print("Account created successfully. Please login.")
                except ValueError as e:
                    print(e)

            elif choice == "3":
                break
        else:
            main_menu(current_user)
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                handle_add_student(manager)

            elif choice == '2':
                handle_add_marks(manager)

            elif choice == '3':
                manager.display_all_students()

            elif choice == '4':
                sid = input('Student ID: ').strip().upper()
                student = manager.find_by_id(sid)
                if student: manager.display_student_card(student)
                else: print(f'Student {sid} not found')

            elif choice == '5':
                sid = input('Student ID: ').strip().upper()
                manager.display_report_card(sid)

            elif choice == '6':
                manager.display_course_filter()        

            elif choice == '7':
                handle_delete(manager)

            elif choice == '8':
                manager.save_to_file()
                print(f"Data saved. Logging out {current_user}.")
                print("Good Bye!")
                current_user = None

            else:
                print('Invalid choice. Enter 1 to 8.')
            

main()