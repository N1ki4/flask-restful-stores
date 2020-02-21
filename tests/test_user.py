from models.user import UserModel
from tests.base_test_class import BaseTest
import json


class UserTest(BaseTest):
    def test_user_initialise(self):
        user = UserModel("test_user", "test1234")

        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "test1234")

    def test_create_user(self):
        with self.app_context():
            user = UserModel("test", "abcd")

            self.assertIsNone(UserModel.find_by_username("test"))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username("test"))
            self.assertIsNotNone(UserModel.find_by_id(1))

    def test_user_register(self):
        # BaseTest has: "self.app = app.test_client" in setUp
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "/register", data={"username": "test", "password": "test1234"}
                )

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("test"))
                self.assertDictEqual(
                    {"message": "User created!"}, json.loads(response.data)
                )

    def test_user_auth(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/register", data={"username": "test", "password": "test1234"}
                )
                auth_response = client.post(
                    "/auth",
                    data=json.dumps({"username": "test", "password": "test1234"}),
                    headers={"Content-Type": "application/json"},
                )

                self.assertIn("access_token", json.loads(auth_response.data).keys())

    def test_user_already_exists(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/register", data={"username": "test", "password": "test1234"}
                )
                response = client.post(
                    "/register", data={"username": "test", "password": "test1234"}
                )

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {"message": "A user with that username already exists"},
                    json.loads(response.data),
                )
