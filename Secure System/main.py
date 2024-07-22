from user import User
from admin import Admin
from database import Database
from artefact import Artefact
from role_based_access import RoleBasedAccessControl

def main():
    # Initialize database and role-based access control
    db = Database(encryption_key=generate_key())
    rbac = RoleBasedAccessControl()

    # Create users
    users = [
        Admin("admin", "adminpass"),  # Admin user
        User("user", "password", "user")  # Regular user
    ]

    current_user = None

    while True:
        if current_user:
            print(f"Logged in as {current_user.username}")
        else:
            print("Not logged in")

        action = input("Enter action (login, logout, create, read, update, delete, exit): ").strip().lower()

        try:
            if action == "login":
                username = input("Username: ")
                password = input("Password: ")

                # Attempt login
                for user in users:
                    if user.login(username, password):
                        current_user = user
                        break
                else:
                    print("Invalid credentials")

            elif action == "logout":
                current_user = None

            elif action == "exit":
                break

            elif current_user:
                if rbac.has_permission(current_user.role, action):
                    if action == "create":
                        title = input("Title: ")
                        content = input("Content: ")
                        artefact = Artefact(title, content, db.encryption_key)
                        db.add_artefact(title, artefact.to_dict())
                        print(f"Artefact '{title}' created")

                    elif action == "read":
                        artefact_name = input("Artefact Name: ")
                        artefact_data = db.read_artefact(current_user.username, artefact_name)
                        if artefact_data:
                            print(f"Artefact: {artefact_data}")
                        else:
                            print(f"Artefact '{artefact_name}' not found")

                    elif action == "update":
                        artefact_name = input("Artefact Name: ")
                        new_content = input("New Content: ")

                        # Retrieve the artefact and update it
                        artefact_data = db.read_artefact(current_user.username, artefact_name)
                        if artefact_data:
                            artefact = Artefact.from_dict(artefact_data, db.encryption_key)
                            artefact.update_data(new_content)

                            updated_data = {
                                "data": artefact.data,
                                "checksum": artefact.calculate_checksum(artefact.data),
                            }

                            db.update_artefact(current_user.username, artefact_name, updated_data)
                            print(f"Artefact '{artefact_name}' updated")
                        else:
                            print(f"Artefact '{artefact_name}' not found")

                    elif action == "delete" and current_user.role == "admin":
                        artefact_name = input("Artefact Name: ")
                        if db.delete_artefact(current_user.username, artefact_name):
                            print(f"Artefact '{artefact_name}' deleted")
                        else:
                            print(f"Artefact '{artefact_name}' not found")

                else:
                    print("Permission denied")
            else:
                print("Please login first")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
