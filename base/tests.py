import mongoengine
from django.test import TestCase
from django.conf import settings


class MongoTestCase(TestCase):
    """Instead of using django 'TestCase' class. Use this in tests.
    It will overwrite the 'setUp' and 'tearDown' functions of django 'TestCase'.

    For example->
    In tests.py :

    from models import App

    class AppCreationTest(MongoTestCase):
      def test(self):
        app = App(name="first_app")
        app.save()
        assert App.objects.first().name == app.name
    In terminal :

    python manage.py test

    Note: Dont forget to specify test db details in settings.
    """

    def setUp(self):
        mongoengine.connection.disconnect()
        mongoengine.connect(
            host=settings.MONGO['host'],
            port=settings.MONGO['port'],
            db=settings.MONGO['db'],
            username=settings.MONGO['username'],
            password=settings.MONGO['password']
            )
        super().setUpClass()

    def tearDown(self):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        connection.drop_database(settings.MONGO['db'])
        disconnect()
        super().tearDownClass()
