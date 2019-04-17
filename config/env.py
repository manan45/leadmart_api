import configparser

config = configparser.ConfigParser()
config.read('application_version.conf')

environment = config.get('ENVIRONMENT', 'environment')
DB_PASSWORD = config.get('ENVIRONMENT', 'db_password')

__local ={
    'db_user': 'root',
    'db_host': 'localhost',
    'db_name': 'leadmart',
    'phost': '127.0.0.1',
    'debug': True,
    'db_password': DB_PASSWORD,
    'port': 8080,
    'SECRET_KEY': 'helloworld'
}

__production = {
    'db_user': 'root',
    'db_host': 'localhost',
    'db_name': 'leadmart',
    'phost': '127.0.0.1',
    'debug': True,
    'post': 8080,
    'SECRET_KEY': 'helloworld'
}

if environment == 'local':
    env = __local
elif environment == 'production':
    env = __production

