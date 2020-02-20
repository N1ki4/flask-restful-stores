from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test_class import BaseTest
import json


class ItemTest(BaseTest):
	def test_post_item(self):
		with self.app() as client:
			with self.app_context():
				StoreModel('test').save_to_db()
				response = client.post('/item/test_item', data=json.dumps({'store_id': 1, 'price': 88.99}),
														  headers={'Content-Type': 'application/json'})
				self.assertEqual(response.status_code, 201)
				self.assertIsNotNone(ItemModel.find_by_name('test_item'))
				self.assertDictEqual({'name': 'test_item', 'price': 88.99, 'store_id': 1},
									 json.loads(response.data))

	def test_get_item_no_auth(self):
		with self.app() as client:
			with self.app_context():
				response = client.get('/item/test')

				self.assertEqual(response.status_code, 401)
				self.assertDictEqual({'message': 'Authorization Required. Request does not contain an access token'},
									 json.loads(response.data))

	def test_item_not_found(self):
		with self.app() as client:
			with self.app_context():
				UserModel('test', 'pass1234').save_to_db()
				auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': 'pass1234'}),
										   			headers={'Content-Type': 'application/json'})

				auth_token = json.loads(auth_request.data)['access_token']
				response = client.get('/item/test', headers={'Content-Type': 'application/json',
															 'Authorization': 'jwt ' + auth_token})
				self.assertEqual(response.status_code, 404)

	def test_get_item(self):
		with self.app() as client:
			with self.app_context():
				StoreModel('test').save_to_db()
				ItemModel('test_item', 88.99, 1).save_to_db()
				UserModel('test', 'pass1234').save_to_db()
				auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': 'pass1234'}),
										   headers={'Content-Type': 'application/json'})

				auth_token = json.loads(auth_request.data)['access_token']
				response = client.get('/item/test_item', headers={'Content-Type': 'application/json',
															 'Authorization': 'jwt ' + auth_token})
				self.assertEqual(response.status_code, 200)
				self.assertDictEqual({'name': 'test_item', 'price': 88.99, 'store_id': 1},
									  json.loads(response.data))

	def test_delete_item(self):
		with self.app() as client:
			with self.app_context():
				StoreModel('test').save_to_db()
				ItemModel('test_item', 88.99, 1).save_to_db()
				response = client.delete('/item/test_item')

				self.assertEqual(response.status_code, 204)

	def test_put_item(self):
		with self.app() as client:
			with self.app_context():
				StoreModel('test').save_to_db()
				ItemModel('test_item', 88.99, 1).save_to_db()
				response = client.put('/item/test_item', data=json.dumps({'price': 13.99, 'store_id': 1}),
														 headers={'Content-Type': 'application/json'})

				self.assertEqual(response.status_code, 200)
				self.assertEqual(ItemModel.find_by_name('test_item').price, 13.99)
				self.assertDictEqual({'name': 'test_item', 'price': 13.99, 'store_id': 1}, json.loads(response.data))

	def test_item_list(self):
		with self.app() as client:
			with self.app_context():
				StoreModel('test').save_to_db()
				ItemModel('test_item1', 10.99, 1).save_to_db()
				ItemModel('test_item2', 13.99, 1).save_to_db()
				response = client.get('/items')

				self.assertEqual(response.status_code, 200)
				self.assertDictEqual({'items': [
					{'name': 'test_item1', 'price': 10.99, 'store_id': 1},
					{'name': 'test_item2', 'price': 13.99, 'store_id': 1}
				]}, json.loads(response.data))
