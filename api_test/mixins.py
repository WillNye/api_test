from uuid import uuid4
import requests


class CreateMixin:

    def test_create_unauthenticated_user(self):
        response = requests.post(self.url, self.post_payload)
        self.assertEqual(response.status_code, 403)

        return response


class PutMixin:

    def test_put_unauthenticated_user(self):
        response = requests.put(f'{self.url}/{self.object_id}', self.post_payload)
        self.assertEqual(response.status_code, 403)

        return response


class PatchMixin:
    patch_payload: dict = None

    def test_patch_unauthenticated_user(self):
        try:
            assert self.patch_payload
        except AssertionError:
            print("patch_payload must be defined in the test setUp method to support the PatchMixin")
            raise

        response = requests.patch(f'{self.url}/{self.object_id}', self.patch_payload)
        self.assertEqual(response.status_code, 403)

        return response


class DeleteMixin:

    def test_delete_valid(self):
        self.delete()

    def test_delete_invalid_id(self):
        response = self.session.delete(f'{self.url}/a01')
        self.assertEqual(response.status_code, 404)

        return response

    def test_delete_id_does_not_exist(self):
        response = self.session.delete(f'{self.url}/{uuid4()}')
        self.assertEqual(response.status_code, 404)

        return response

    def test_delete_unauthenticated_user(self):
        response = requests.delete(f'{self.url}/{self.object_id}')
        self.assertEqual(response.status_code, 403)

        return response


class ListMixin:

    def test_list_filter(self, filter_key: str):
        filter_val = self.object[filter_key]
        response = self.session.get(self.url, params={filter_key: filter_val})
        self.assertTrue(response.ok)
        response_objs = response.json()
        self.assertTrue(all(obj[filter_key] == filter_val for obj in response_objs['results']))

        return response

    def test_list_sort(self, sort_param: str, sort_key: str):
        response = self.session.get(self.url, params={sort_param: sort_key})
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

    def test_retrieve_valid(self):
        response = self.session.get(f'{self.url}/{self.object_id}')
        self.assertTrue(response.ok)

