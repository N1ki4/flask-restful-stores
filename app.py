import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "nick"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # auth
api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")


@app.errorhandler(JWTError)
def auth_error(err):
    return (
        jsonify(
            {
                "message": "Authorization Required. Request does not contain an access token"
            }
        ),
        401,
    )


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
