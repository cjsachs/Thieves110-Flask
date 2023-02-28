import os

# CONFIG SECTION
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
        'christiana@thieves.com': {
            'name': 'Christian',
            'password': 'test123'
        },
        'dylank@thieves.com': {
            'name': 'Dylan',
            'password': 'ilovemydog'
        }
    }