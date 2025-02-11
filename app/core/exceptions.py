from asyncpg import (
    InvalidAuthorizationSpecificationError,
    InvalidCatalogNameError,
)
from google.api_core.exceptions import Forbidden
from google.auth.exceptions import GoogleAuthError


class ErrorWithGoogleCloudAuthentication(Exception):
    def __init__(self, exception: GoogleAuthError):
        message = (
            f"Failed to create Google Secret Manager client. "
            f"Trigger exception: {exception.__class__.__name__}.\n"
            f"Message: {exception}"
        )
        super().__init__(message)


class DoesNotHavePermissionForGoogleCloudSecret(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidUsernameOrPasswordForDatabase(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class WrongDatabaseName(Exception):
    def __init__(self, message: str):
        super().__init__(message)
