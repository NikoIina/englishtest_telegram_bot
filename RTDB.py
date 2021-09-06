import pyrebase
import telebot
from telebot import types

class RTDB:

    def __init__(self):
        config = {
            "apiKey": "Your-API-key",
            "authDomain": "Your-app-ID.firebaseapp.com",
            "databaseURL": 'https://Your-App-URL.firebasedatabase.app/',
            "storageBucket": "Your-App-ID.appspot.com",
            "serviceAccount": 'database_data.json'
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.database = self.db.get()
        self.storage = self.firebase.storage()
        self.dict = {}
        self.questions = []
        self.points = []
        self.index = 0

        for i in self.database.each():
            self.dict[i.key()] = i.val()

    def create_list(self):
        for i in self.database.each():
            self.questions.append(i.key())
        self.index = 0
        self.points = []

    def create_question(self, key):
        return self.dict[key]['Question']

    def get_answers(self, key):
        if 'Answers' in self.dict[key]:
            return self.dict[key]['Answers']
        else:
            pass

    def get_points(self, key):
        return self.dict[key]['Points']

    def get_correct(self, key):
        return self.dict[key]['Correct']

    def count_points(self, key, call):
        if call.data == self.get_correct(key):
            self.points.append(self.dict[key]['Points'])
        self.index += 1

    def count_points_text(self, key, message):
        if str(message).lower() == self.get_correct(key):
            self.points.append(self.dict[key]['Points'])
        self.index = self.index + 1

    def get_picture(self, key):
        if 'PicName' in self.dict[key]:
            name = self.dict[key]['PicName']
            token = self.dict[key]['PicToken']
            picture = self.storage.child(name).get_url(token)
            return picture
        else:
            pass

    def get_audio(self, key):
        if 'AudioName' in self.dict[key]:
            name = self.dict[key]['AudioName']
            token = self.dict[key]['AudioToken']
            audio = self.storage.child(name).get_url(token)
            return audio
        else:
            pass