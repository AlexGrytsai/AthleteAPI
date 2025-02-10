from google.auth.exceptions import GoogleAuthError


class ErrorWithGoogleCloudAuthentication(Exception):
    def __init__(self, exception: GoogleAuthError):
        message = (
            f"Failed to create Google Secret Manager client. "
            f"Trigger exception: {exception.__class__.__name__}.\n"
            f"Message: {exception}"
        )
        super().__init__(message)
