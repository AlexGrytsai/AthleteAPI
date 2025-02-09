from abc import ABC, abstractmethod

from typing import Union, TypeAlias, Optional

from google.auth.exceptions import DefaultCredentialsError, GoogleAuthError
from google.cloud import secretmanager

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
    def __init__(self):
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
        pass
