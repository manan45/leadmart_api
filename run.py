from app import APP
from config import env
print(env)

if __name__ == "__main__":
    APP.run(port=env['port'], debug=env['debug'], host=env['phost'])

