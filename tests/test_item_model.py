from models.item import ItemModel
from models.store import StoreModel
from tests.base_test_class import BaseTest


class ItemTest(BaseTest):
    def test_item_initialise(self):
        with self.app_context():
            StoreModel("test").save_to_db()
            item = ItemModel("test", 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name("test"))

            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name("test"))
            self.assertEqual(item.name, "test")
            self.assertEqual(item.price, 19.99)
            self.assertEqual(item.store_id, 1)

            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name("test"))

    def test_item_store_relationship(self):
        with self.app_context():
            store = StoreModel("test_store")
            item = ItemModel("test", 19.99, 1)
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, "test_store")

    def test_item_json(self):
        with self.app_context():
            StoreModel("test").save_to_db()
            item = ItemModel("test", 19.99, 1)
            item.save_to_db()
            expected_json = {
                "name": "test",
                "price": 19.99,
                "store_id": 1,
            }
            self.assertDictEqual(item.json(), expected_json)
