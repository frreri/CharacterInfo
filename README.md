# CharacterInfo
Website built on Python Flask framework. Utilizes Blizzard's community APIs to get info about WoW characters.
Currently deployed as https://frer.se

To be able to run this a config.py file needs to be created in the repository root containing the following:
```
class AppConfig:
    SECRET_KEY = 'A secret key for your app'
    SQLALCHEMY_DATABASE_URI = 'SQL alchemy db uri'
    MAIL_SERVER = 'server'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'email'
    MAIL_PASSWORD = 'pass'

class APIconfig:
    CLIENT_ID = 'Your Blizzard api client id'
    CLIENT_SECRET = 'Your Blizzard api client secret'

class MySQLconfig:
    MYSQL_HOST = 'host'
    MYSQL_USER = 'user'
    MYSQL_PASSWORD = 'pass'
    MYSQL_DATABASE = 'db'
```
Before running the application, create the required database tables by running create_tables.py

Right now the application does not contain database table creation for some of its features.
I will change all database communication to SQLAlchemy in the near future which will fix that.

User accounts and logged in features are in the works.

HEJ HEJ