import os
from abc import ABC, abstractmethod
from typing import Union, TypeAlias, Optional

from dotenv import load_dotenv
from google.api_core.exceptions import NotFound
from google.auth.exceptions import DefaultCredentialsError, GoogleAuthError
from google.cloud import secretmanager

load_dotenv()

DefaultValueType: TypeAlias = Union[str, int, None]


class SecretKeyBase(ABC):
    """
    Abstract base class for secret key management.

    This class provides a blueprint for implementing secret key retrieval.
    """

    @abstractmethod
    def get_secret_key(
        self, secret_key: str, default_value: Optional[DefaultValueType] = None
    ) -> DefaultValueType:
        """
        Retrieves a secret key.

        Args:
        - secret_key (str): The key to retrieve.
        - default_value (DefaultValueType, optional):
                            The default value to return if the key is not
                            found. Defaults to None.

        Returns:
        - DefaultValueType: The retrieved secret key or the default value.
        """
        pass


class SecretKeyGoogleCloud(SecretKeyBase):
    """
    A concrete implementation of SecretKeyBase for Google Cloud Secret Manager.

    This class provides a way to retrieve secret keys from Google Cloud
    Secret Manager.
    """

    def __init__(self):
        """
        Initializes the SecretKeyGoogleCloud instance.

        Creates a SecretManagerServiceClient instance and assigns it
        to the client attribute.
        If the default credentials are not found, raises a GoogleAuthError.
        """
        try:
            self.client = secretmanager.SecretManagerServiceClient()
        except DefaultCredentialsError as exc:
            raise GoogleAuthError(
                f"Failed to create secret manager client: {exc}"
            )

    def get_secret_key(
        self,
        secret_key: str,
        default_value: Optional[DefaultValueType] = None,
    ) -> DefaultValueType:
        try:
            google_cloud_project_id = os.getenv("GOOGLE_PROJECT_ID")

            parent = (
                f"projects/{google_cloud_project_id}/secrets/"
                f"{secret_key}/versions/latest"
            )

            secret_value = self.client.access_secret_version(
                request={"name": parent}
            )
            return secret_value.payload.data.decode("UTF-8")

        except (NotFound, AttributeError):
            return default_value


secret = SecretKeyGoogleCloud()
