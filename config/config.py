import os

class Config:
    SECRET_KEY = os.urandom(24)
    DB_CONFIG = {
        'host': "127.0.0.1",
        'user': "root",
        'password': "",
        'database': "asistenciass",
        'cursorclass': 'DictCursor'
    }


"""

German

class Config:
    SECRET_KEY = os.urandom(24)
    DB_CONFIG = {
        'host': "127.0.0.1",
        'user': "root",
        'password': "7003",
        'database': "asistencia",
        'cursorclass': 'DictCursor'
    }

"""    
