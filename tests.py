import mock
import unittest
import server
from server import app

# TODO:
# Mock API calls

class ActivityMicroserviceTests(unittest.TestCase):
    """Test activity microservice."""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_valid_entries(self):
        result = self.client.get("/activity?zipcode=94704&participants=3")
        data = result.json
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["city"], "Berkeley")

    def test_no_entries(self):
        result = self.client.get("/activity")
        self.assertEqual(result.status_code, 400)
        self.assertIn(b"error", result.data)

    def test_invalid_zipcode_alpha(self):
        result = self.client.get("/activity?zipcode=a&participants=3")
        self.assertEqual(result.status_code, 400)
        self.assertIn(b"error", result.data)

    def test_invalid_zipcode(self):
        result = self.client.get("/activity?zipcode=00000&participants=3")
        self.assertEqual(result.status_code, 500)
        self.assertIn(b"error", result.data)

    def test_invalid_participants_alpha(self):
        result = self.client.get("/activity?zipcode=94704&participants=a")
        self.assertEqual(result.status_code, 400)
        self.assertIn(b"error", result.data)

    def test_invalid_participants(self):
        result = self.client.get("/activity?zipcode=94704&participants=6")
        self.assertEqual(result.status_code, 400)
        self.assertIn(b"error", result.data)

    def test_invalid_zipcode_and_participants(self):
        result = self.client.get("/activity?zipcode=a&participants=0")
        self.assertEqual(result.status_code, 400)
        self.assertIn(b"error", result.data)

    @mock.patch("server.requests.get")
    def test_success_response(self, requests_patch):
        # Construct the mock for a successful response
        ok_response_mock = mock.MagicMock()
        type(ok_response_mock).status_code = mock.PropertyMock(return_value=200)
        fake_zip_json = {"places": [{"place name": "San Francisco"}]}
        fake_activity_json = {"activity": "Go for a walk"}
        ok_response_mock.json.side_effect = [fake_zip_json, fake_activity_json]

        # Attach the ok response to the requests patch
        requests_patch.return_value = ok_response_mock

        result = self.client.get("/?zipcode=94301&participants=1")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.json,
            {"city": "San Francisco", "activity": "Go for a walk"}
        )


if __name__ == "__main__":
    unittest.main()
