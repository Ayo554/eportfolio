from artefact import Artefact
from database import Database

class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role
        self.artefacts = []

    def add_artefact(self, db, artefact):
        if isinstance(artefact, Artefact):
            result = db.add_artefact(self.username, artefact.to_dict())
            if result:
                self.artefacts.append(artefact)
            return result
        return False

    def remove_artefact(self, db, artefact_name):
        result = db.delete_artefact(self.username, artefact_name)
        if result:
            self.artefacts = [a for a in self.artefacts if a.name != artefact_name]
        return result

    def get_artefact(self, db, artefact_name):
        artefact_dict = db.read_artefact(self.username, artefact_name)
        if artefact_dict:
            return Artefact.from_dict(artefact_dict, self.password)
        return None

    def list_artefacts(self, db):
        return db.list_user_artefacts(self.username)
