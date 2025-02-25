import unittest
from http import HTTPStatus

from remote_eink.tests._common import AppTestBase


class TestDisplayApi(AppTestBase):
    """
    Tests for the `/display` endpoint.
    """

    def test_list(self):
        for _ in range(10):
            self.create_display_controller()
        result = self.client.get("/display")
        self.assertEqual(HTTPStatus.OK, result.status_code)
        self.assertCountEqual(
            [{"id": controller.identifier} for controller in self.display_controllers.values()], result.json
        )

    def test_get(self):
        for _ in range(5):
            self.create_display_controller()
        display_controller = self.create_display_controller(number_of_images=10)
        for _ in range(5):
            self.create_display_controller()

        result = self.client.get(f"/display/{display_controller.identifier}")
        self.assertEqual(HTTPStatus.OK, result.status_code)
        self.assertEqual(display_controller.identifier, result.json["id"])
        self.assertCountEqual(
            (image.identifier for image in display_controller.image_store.list()),
            (image["id"] for image in result.json["images"]),
        )

    def test_get_not_exist(self):
        result = self.client.get(f"/display/does-not-exist")
        self.assertEqual(HTTPStatus.NOT_FOUND, result.status_code)

    def test_get_with_no_images(self):
        display_controller = self.create_display_controller(number_of_images=0)
        result = self.client.get(f"/display/{display_controller.identifier}")
        self.assertEqual(HTTPStatus.OK, result.status_code)
        self.assertEqual([], result.json["images"])
        self.assertIsNone(result.json["currentImage"])


if __name__ == "__main__":
    unittest.main()
