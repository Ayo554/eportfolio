from artefact import Artefact
import pickle
import os

class Database:
    def __init__(self, encryption_key):
        # Initializes an in-memory database with encryption key
        self.encryption_key = encryption_key
        self.data = {}  # In-memory database
        self.db_file = 'database.pkl'

    def add_artefact(self, username, artefact_dict):
        # Adds an artefact to the database
        if username not in self.data:
            self.data[username] = {}
        self.data[username][artefact_dict['name']] = artefact_dict
        return True

    def read_artefact(self, username, artefact_name):
        # Reads an artefact from the database
        artefact_dict = self._fetch_from_db(username, artefact_name)
        if artefact_dict:
            return Artefact.from_dict(artefact_dict, self.encryption_key)
        return None

    def update_artefact(self, username, artefact_name, new_data):
        # Updates an artefact's data in the database
        artefact_dict = self._fetch_from_db(username, artefact_name)
        if artefact_dict:
            artefact = Artefact.from_dict(artefact_dict, self.encryption_key)
            artefact.update_data(new_data)
            self._store_in_db(username, artefact_name, artefact.to_dict())
            return True
        return False

    def delete_artefact(self, username, artefact_name):
        # Deletes an artefact from the database
        if username in self.data and artefact_name in self.data[username]:
            del self.data[username][artefact_name]
            return True
        return False

    def _fetch_from_db(self, username, artefact_name):
        # Fetches an artefact dictionary from the in-memory database
        return self.data.get(username, {}).get(artefact_name)

    def _store_in_db(self, username, artefact_name, artefact_dict):
        # Stores an artefact dictionary in the in-memory database
        if username not in self.data:
            self.data[username] = {}
        self.data[username][artefact_name] = artefact_dict

    def load_database(self):
        # Loads the database from a file
        if os.path.exists(self.db_file):
            with open(self.db_file, 'rb') as file:
                self.data = pickle.load(file)
        else:
            self.data = {}

    def save_database(self):
        # Saves the database to a file
        with open(self.db_file, 'wb') as file:
            pickle.dump(self.data, file)

    def list_user_artefacts(self, username):
        # Lists all artefacts for a given user
        return list(self.data.get(username, {}).keys())
