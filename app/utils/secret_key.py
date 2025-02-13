import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv
from google.api_core.exceptions import NotFound, Forbidden
from google.auth.exceptions import GoogleAuthError
from google.cloud.secretmanager_v1 import (
    SecretManagerServiceClient,
)

from app.core.exceptions import (
    ErrorWithGoogleCloudAuthentication,
    DoesNotHavePermissionForGoogleCloudSecret,
)
from app.utils.decorators import memory_profiler_class

load_dotenv()

logger = logging.getLogger()


class SecretKeyBase(ABC):
    """
    Abstract base class for secret key management.

    This class provides a blueprint for implementing secret key retrieval.
    """

    @abstractmethod
    async def get_secret_key(self, secret_key: str, default_value: str) -> str:
        """
        Retrieves a secret key.

        Args:
        - secret_key (str): The key to retrieve.
        - default_value (str): The default value to return if the key is not
                               found. Defaults to None.

        Returns:
        - str: The retrieved secret key or the default value.
        """
        pass


class MockSecretKey(SecretKeyBase):
    async def get_secret_key(
        self, secret_key: str, default_value: str = "mock_value"
    ) -> str:
        return default_value


class SecretKeyGoogleCloud(SecretKeyBase):
    """
    A concrete implementation of SecretKeyBase for Google Cloud Secret Manager.

    This class provides a way to retrieve secret keys from Google Cloud
    Secret Manager.
    """

    __slots__ = ("_client",)

    def __init__(self, client: Optional[SecretManagerServiceClient]):
        self._client = client

    async def get_secret_key(
        self,
        secret_key: str,
        default_value: str,
    ) -> str:
        if not self._client:
            return default_value

        try:
            google_cloud_project_id = os.getenv("GOOGLE_PROJECT_ID")

            parent = (
                f"projects/{google_cloud_project_id}/secrets/"
                f"{secret_key}/versions/latest"
            )

            secret_value = self._client.access_secret_version(
                request={"name": parent}
            )
            return str(secret_value.payload.data.decode("UTF-8"))
        except Forbidden as exc:
            error_massage = (
                f"Problem with permission for Google Cloud Secret. "
                f"Trigger exception: {exc.__class__.__name__}.\n"
                f"Message: {exc}"
            )
            logger.error(error_massage)
            raise DoesNotHavePermissionForGoogleCloudSecret(error_massage)

        except (NotFound, AttributeError) as exc:
            error_massage = (
                f"Failed to get secret from Google Cloud Secret. "
                f"Trigger exception: {exc.__class__.__name__}.\n"
                f"Message: {exc}"
            )
            logger.warning(error_massage)
            return default_value


def create_google_secret_client() -> Optional[SecretManagerServiceClient]:
    try:
        return SecretManagerServiceClient()
    except GoogleAuthError as exc:
        error_massage = (
            f"Failed to create Google Secret Manager client."
            f"Trigger exception: {exc.__class__.__name__}.\n"
            f"Message: {exc}"
        )
        logger.error(error_massage)
        raise ErrorWithGoogleCloudAuthentication(error_massage)
