from flask_restful import Api
from routes import endpoints


class EndpointManager():
    api_version = '1.0'

    def __init__(self, app):
        self.api = Api(app)

    def load(self):
        for endpoint in endpoints:
            args = [endpoint[0]]
            for i in range(1, len(endpoint)):
                if i != 0:
                    args.append('/' + self.api_version + endpoint[i])
            self.api.add_resource(*args)
        return 0

