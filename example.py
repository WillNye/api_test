from faker import Faker
import requests

from api_test import BaseAPICase, CreateMixin, DeleteMixin, ListMixin, PatchMixin, PutMixin, RetrieveMixin


class ExampleAPIBase(BaseAPICase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = 'https://example.com/api'
        cls.session = requests.Session()
        cls.session.headers = {'Authorization': 'Bearer ...'}
        super().setUpClass()


class TestUser(CreateMixin, DeleteMixin, ListMixin, PatchMixin, PutMixin, RetrieveMixin, ExampleAPIBase):

    @classmethod
    def setUpClass(cls):
        cls.route = 'user'
        cls.delete_on_teardown = False
        super().setUpClass()

    def setUp(self):
        fake = Faker()
        self.post_payload = {
            "name": f"{fake.first_name()} {fake.last_name()}",
            "email": fake.email()
        }
        self.patch_payload = {"name": f"{fake.first_name()} {fake.last_name()}"}
        super().setUp()
