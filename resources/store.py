from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return "", 404

    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {"message": f"A store {name} already exists."}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error creating store."}, 500
        return store.json(), 201

    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return "", 204


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
