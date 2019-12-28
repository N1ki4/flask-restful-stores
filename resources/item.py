import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price",
			type=float,
			required=True,
			help="Price came with errors or field is blank!"
	)
	parser.add_argument("store_id",
			type=int,
			required=True,
			help="Every item need to have store id."
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {"message": "Item not found"}, 404


	def post(self, name):
		if ItemModel.find_by_name(name):
			return {"message": f"An item '{name}' already exists."}, 400

		data = Item.parser.parse_args()

		item = ItemModel(name, **data) # data["price"], data["store_id"]

		try:
			item.save_to_db()
		except: 												## Server error
			return {"message": "An error occured inserting item."}, 500 

		return item.json(), 201


	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {"message": "Item deleted."}


	def put(self, name):
		data = Item.parser.parse_args()
		
		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, **data)
		else:
			item.price = data["price"]
		
		item.save_to_db()

		return item.json()


class ItemList(Resource):
	def get(self):
		## "items": list(map(lambda x: x.json(), ItemModel.query.all()))
		return {"items": [i.json() for i in ItemModel.query.all()]}
