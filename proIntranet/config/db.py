import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'intranet',
        'USER': 'postgres',
        'PASSWORD': 'P0$tGr3$..',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
