import os
import unittest
from unittest.mock import patch, MagicMock

from google.api_core.exceptions import NotFound

from app.utils.secret_key import SecretKeyGoogleCloud


class TestSecretKeyGoogleCloud(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.secret = SecretKeyGoogleCloud(client=self.mock_client)

    def test_init_success(self):
        self.assertIsNotNone(self.secret.client)
        self.mock_client.assert_not_called()

    @patch.dict(os.environ, {"GOOGLE_PROJECT_ID": "test"})
    def test_get_secret_key_success(self):
        mock_secret_value = MagicMock()
        mock_secret_value.payload.data.decode.return_value = "my-secret-value"
        self.mock_client.access_secret_version.return_value = mock_secret_value

        secret = self.secret.get_secret_key("my-secret")
        self.assertEqual(secret, "my-secret-value")
        self.mock_client.access_secret_version.assert_called_once_with(
            request={"name": "projects/test/secrets/my-secret/versions/latest"}
        )

    @patch.dict(os.environ, {"GOOGLE_PROJECT_ID": "test-project"})
    def test_get_secret_key_not_found(self):
        self.mock_client.access_secret_version.side_effect = NotFound(
            "Secret not found"
        )

        secret = self.secret.get_secret_key(
            "non-existent-secret", default_value="default"
        )
        self.assertEqual(secret, "default")

    def test_get_secret_key_no_project_id(self):
        self.mock_client.access_secret_version.side_effect = AttributeError(
            "Project ID not found"
        )

        secret = self.secret.get_secret_key(
            "without-project-id", default_value="default"
        )
        self.assertEqual(secret, "default")
