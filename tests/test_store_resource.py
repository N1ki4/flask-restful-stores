from tests.base_test_class import BaseTest
from models.store import StoreModel
from models.item import ItemModel
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test"))
                self.assertDictEqual(
                    {"name": "test", "items": []}, json.loads(response.data)
                )

    def test_create_store_already_exist(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                response = client.post("/store/test")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {"message": "A store test already exists."},
                    json.loads(response.data),
                )

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                self.assertIsNotNone(StoreModel.find_by_name("test"))

                response = client.delete("/store/test")
                self.assertEqual(response.status_code, 204)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                response = client.get("/store/test")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {"name": "test", "items": []}, json.loads(response.data)
                )

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/test")

                self.assertEqual(response.status_code, 404)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()
                response = client.get("/store/test")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {
                        "name": "test",
                        "items": [{"name": "test", "price": 19.99, "store_id": 1}],
                    },
                    json.loads(response.data),
                )

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test1").save_to_db()
                StoreModel("test2").save_to_db()

                response = client.get("/stores")

                self.assertDictEqual(
                    {
                        "stores": [
                            {"name": "test1", "items": []},
                            {"name": "test2", "items": []},
                        ]
                    },
                    json.loads(response.data),
                )

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test1").save_to_db()
                StoreModel("test2").save_to_db()
                ItemModel("test123", 19.99, 2).save_to_db()

                response = client.get("/stores")

                self.assertDictEqual(
                    {
                        "stores": [
                            {"name": "test1", "items": []},
                            {
                                "name": "test2",
                                "items": [
                                    {"name": "test123", "price": 19.99, "store_id": 2}
                                ],
                            },
                        ]
                    },
                    json.loads(response.data),
                )
