from models.item import ItemModel
from models.store import StoreModel
from tests.base_test_class import BaseTest


class StoreTest(BaseTest):

	def test_store_initialise(self):
		store = StoreModel('test')

		self.assertEqual(store.name, 'test')

	def test_store_no_items(self):
		store = StoreModel('test')

		self.assertEqual(store.items.all(), [])

	def test_store_save_delete_to_db(self):
		with self.app_context():
			store = StoreModel('test')

			self.assertIsNone(StoreModel.find_by_name('test'))

			store.save_to_db()
			self.assertIsNotNone(StoreModel.find_by_name('test'))

			store.delete_from_db()
			self.assertIsNone(StoreModel.find_by_name('test'))

	def test_store_with_items(self):
		with self.app_context():
			store = StoreModel('test')
			store.save_to_db()
			ItemModel('test1', 19.99, 1).save_to_db()
			ItemModel('test2', 15.99, 1).save_to_db()

			self.assertEqual(len(store.items.all()), 2)

	def test_store_json(self):
		with self.app_context():
			store = StoreModel('test_store')
			store.save_to_db()
			ItemModel('test1', 19.99, 1).save_to_db()
			ItemModel('test2', 15.99, 1).save_to_db()
			expected_json = {
				'items': [
					{'name': 'test1', 'price': 19.99, 'store_id': 1},
					{'name': 'test2', 'price': 15.99, 'store_id': 1},
				],
				'name': 'test_store',
			}

			self.assertDictEqual(store.json(), expected_json)
