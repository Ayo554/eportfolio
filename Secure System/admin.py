from user import User
from artefact import Artefact
from database import Database

class Admin(User):
    def __init__(self, username, password):
        # Initializes an Admin user with a role of "admin"
        super().__init__(username, password, "admin")

    def create_artefact(self, db, name, content, key):
        # Creates a new artefact and adds it to the database
        artefact = Artefact(name, content, key)
        return db.add_artefact(self.username, artefact.to_dict())

    def delete_artefact(self, db, artefact_name):
        # Deletes an artefact from the database
        return db.delete_artefact(self.username, artefact_name)
