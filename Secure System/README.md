Command-Line Application
This project is a Python-based command-line application designed for managing artefacts. It supports user roles with different permissions, artefact creation, encryption, and testing.

Project Structure
admin.py: Contains the Admin class for administrative tasks.
artefact.py: Defines the Artefact class with encryption and checksum functionality.
checksum.py: Provides checksum generation utilities.
database.py: Implements the Database class for artefact storage and retrieval.
encryption.py: Manages encryption and decryption operations.
main.py: The main script to run the application.
timestamp.py: Utility for timestamp management.
user.py: Contains the User class with artefact management methods.
role_based_access.py: Defines role-based access control for different actions.
tests/: Contains unit tests for the application.


Running the Application
Start the Application:

python main.py
The application will prompt you for various actions such as login, create, read, update, delete, and exit. Follow the instructions in the command line interface to interact with the application.

Log In:

Admin: Use the username admin and password adminpass.
User: Use the username user and password password.
Example interaction:


Enter action (login, logout, create, read, update, delete, exit): login
Username: admin
Password: adminpass
Perform Actions:

Create: Add a new artefact.
Read: Retrieve an artefact by its name.
Update: Modify the content of an existing artefact.
Delete: Remove an artefact (Admin only).
Testing
To ensure the application is functioning correctly, automated tests are provided. These tests cover various components and functionalities of the application.

Run Tests:
pytest
This command will run all unit tests and provide a summary of test results.

References
Cryptography Library: cryptography
Python Documentation: Python 3.x Documentation
pytest: pytest Documentation

Citations
Code Style Guide: PEP 8
Academic Integrity: University of Essex Referencing Guide