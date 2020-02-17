"""
Base Test Class

This class must be parent of each non unit test.
This class creates database and cleans it after tests passed.
"""
from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stores_user:stores@localhost:5432/stores_test'
		"""
		Loads all app  variables and config, pretends to be running app,
		everything that interact with this app is able to run, as is the app is running.
		"""
		with app.app_context():
			db.init_app(app)
			db.create_all()
		# create test client
		self.app = app.test_client
		# create access to app context after setUp in other tests
		self.app_context = app.app_context

	def tearDown(self):
		with app.app_context():
			db.session.remove()
			db.drop_all()
