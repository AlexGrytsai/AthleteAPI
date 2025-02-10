import unittest
from unittest.mock import patch, MagicMock

from app.core.config import DatabaseSettings
from app.utils.secret_key import SecretKeyBase
from app.utils.validators import DBParamValidator


class TestDatabaseSettings(unittest.TestCase):
    def setUp(self):
        self.mock_secret = MagicMock(spec=SecretKeyBase)
        self.mock_validator = MagicMock(spec=DBParamValidator)

        self.db_settings = DatabaseSettings(
            database_scheme="postgresql",
            secret=self.mock_secret,
            validator_parameters=self.mock_validator,
        )

    @patch("app.core.config.SecretKeyBase")
    @patch("app.core.config.DBParamValidator")
    def test_url(self, mock_db_param_validator, mock_secret_key_base):
        self.mock_secret.get_secret_key.return_value = "test"
        self.mock_validator.validate_parameter_from_secret.return_value = (
            "test"
        )

        expected_url = "postgresql://test:test@test:test/test"
        self.assertEqual(self.db_settings.url, expected_url)

    @patch("app.core.config.SecretKeyBase")
    @patch("app.core.config.DBParamValidator")
    def test_get_db_param(self, mock_db_param_validator, mock_secret_key_base):
        self.mock_secret.get_secret_key.return_value = "test_value"
        self.mock_validator.validate_parameter_from_secret.return_value = (
            "test_value"
        )

        result = self.db_settings._get_db_param(
            "USER", default="default_value"
        )

        self.assertEqual(result, "test_value")
        self.mock_secret.get_secret_key.assert_called_with(
            "USER", "default_value"
        )
        self.mock_validator.validate_parameter_from_secret.assert_called_with(
            param="USER", value="test_value"
        )

    @patch("app.core.config.SecretKeyBase")
    @patch("app.core.config.DBParamValidator")
    def test_invalid_param_type(
        self, mock_db_param_validator, mock_secret_key_base
    ):
        self.mock_secret.get_secret_key.return_value = 123
        self.mock_validator.validate_parameter_from_secret.return_value = 123

        result = self.db_settings._get_db_param("PORT", default="5432")
        self.assertEqual(result, 123)
        self.mock_secret.get_secret_key.assert_called_with("PORT", "5432")
        self.mock_validator.validate_parameter_from_secret.assert_called_with(
            param="PORT", value=123
        )
