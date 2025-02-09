import os
from abc import ABC, abstractmethod
from typing import Union, TypeAlias, Optional

from dotenv import load_dotenv
from google.api_core.exceptions import NotFound
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import SecretManagerServiceClient

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

    def __init__(self, client: Optional[SecretManagerServiceClient]):
        """
        Initializes a new instance of the SecretKeyGoogleCloud class.

        Args:
            client (Optional[SecretManagerServiceClient]): The client used
            to interact with Google Cloud Secret Manager.
        """
        self.client = client

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


def create_google_secret_client() -> Optional[SecretManagerServiceClient]:
    try:
        return SecretManagerServiceClient()
    except DefaultCredentialsError:
        return None


google_client = create_google_secret_client()

secret = SecretKeyGoogleCloud(client=google_client)
