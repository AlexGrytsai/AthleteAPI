from asyncpg import InvalidAuthorizationSpecificationError
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
    def __init__(self, exception: Forbidden):
        message = (
            f"Problem with permission for Google Cloud Secret. "
            f"Trigger exception: {exception.__class__.__name__}.\n"
            f"Message: {exception}"
        )
        super().__init__(message)


class InvalidUsernameOrPasswordForDatabase(Exception):
    def __init__(self, exception: InvalidAuthorizationSpecificationError):
        message = (
            f"Was provided invalid username or password "
            f"for connection to Database. Trigger exception: "
            f"{exception.__class__.__name__}.\n"
            f"Message: {exception}"
        )
        super().__init__(message)
