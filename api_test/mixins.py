from uuid import uuid4
import requests


class DeleteMixin:

    def test_valid_delete(self):
        self.delete()

    def test_invalid_id(self):
        response = self.session.delete(f'{self.base_url}/{self.route}/a01')
        self.assertEqual(response.status_code, 404)

        return response

    def test_id_does_not_exist(self):
        response = self.session.delete(f'{self.base_url}/{self.route}/{uuid4()}')
        self.assertEqual(response.status_code, 404)

        return response

    def test_unauth(self):
        response = requests.delete(f'{self.base_url}/{self.route}/{self.object_id}')
        self.assertEqual(response.status_code, 401)

        return response


class ListMixin:

    def test_filter(self, filter_key: str):
        filter_val = self.object[filter_key]
        response = self.session.get(f'{self.base_url}/{self.route}', params={filter_key: filter_val})
        self.assertTrue(response.ok)
        response_objs = response.json()
        self.assertTrue(all(obj[filter_key] == filter_val for obj in response_objs['results']))

        return response

    def test_sort(self, sort_param: str, sort_key: str):
        response = self.session.get(f'{self.base_url}/{self.route}', params={sort_param: sort_key})
        self.assertTrue(response.ok)

        if sort_key.startswith('-'):
            reverse = True
            sort_key = sort_key[1:]
        else:
            reverse = False

        response_objs = response.json()
        response_vals = [obj[sort_key] for obj in response_objs['results']]
        self.assertEqual(response_vals, sorted(response_vals, reverse=reverse))

        return response


class RetrieveMixin:

    def test_valid_retrieve(self):
        response = self.session.get(f'{self.base_url}/{self.route}/{self.object_id}')
        self.assertTrue(response.ok)

