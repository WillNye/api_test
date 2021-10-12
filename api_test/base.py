from unittest import TestCase

import requests


class BaseAPICase(TestCase):
    base_url: str = None
    route: str = None
    session: requests.Session = None
    post_payload: dict = None
    object_id_key = "id"

    @property
    def object_id(self):
        return self.object[self.object_id_key]  # Override if this is not how the id is retrieved

    def create(self) -> requests.Response:
        response = self.session.post(f'{self.base_url}/{self.route}', json=self.post_payload)
        self.assertTrue(response.ok)
        return response

    def delete(self):
        response = self.session.delete(f'{self.base_url}/{self.route}/{self.object_id}')
        self.assertTrue(response.ok)

    def setUp(self):
        assert self.base_url
        assert self.route
        assert self.post_payload

        super(BaseAPICase, self).setUp()
        if not self.session:
            self.session = requests.Session()

        response = self.create()
        res_obj = response.json()
        self.object = res_obj

    def tearDown(self):
        super(BaseAPICase, self).tearDown()
        self.delete()
