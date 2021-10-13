from faker import Faker
import requests

from api_test.base import BaseAPICase
from api_test.mixins import DeleteMixin, ListMixin, RetrieveMixin


class ExampleAPIBase(BaseAPICase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = 'https://example.com/api'
        cls.session = requests.Session()
        cls.session.headers = {'Authorization': 'Bearer ...'}
        super().setUpClass()


class BaseUser(ExampleAPIBase):

    @classmethod
    def setUpClass(cls):
        cls.route = 'messages/broadcasts'
        cls.delete_on_teardown = False
        super().setUpClass()

    def setUp(self):
        fake = Faker()
        self.post_payload = {
            "name": " ".join(fake.words(3)),
            "email": fake.email()
        }
        super().setUp()


class RetrieveUser(RetrieveMixin, BaseUser):
    pass

