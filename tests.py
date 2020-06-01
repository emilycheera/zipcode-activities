import unittest
from server import app
import json

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


if __name__ == "__main__":
    unittest.main()