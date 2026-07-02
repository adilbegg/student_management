from auth import login
from auth import create_account
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
                    print(f"Welcome, {username}!")
                    current_user = username
                    #manager = StudentManager()

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

            if choice == '8':
                print(f"Data saved. Logging out {current_user}.")
                print("Good Bye!")
                current_user = None
            # Logout: manager.save_to_file(), current_user = None
            

main()