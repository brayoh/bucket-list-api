from flask_restful import Resource


class AccountsManager(Resource):
    """docstring for AccountsManager."""
    def get(self):
        return {"route": "login"}

    def post(self):
        return {"route": "register"}
