class DatabaseError(Exception):
    """Basic class for all errors associated with the database."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidUsernameOrPasswordForDatabase(DatabaseError):
    """Error: the wrong login or password for connecting to the database."""


class WrongDatabaseName(DatabaseError):
    """Error: The incorrect name of the database is indicated."""


class DatabaseConnectionErrorWrongHostOrPort(DatabaseError):
    """Error: Incorrect host or port for connecting to the database."""


class ProblemWithConnectionToDatabaseServer(DatabaseError):
    """Error: problem with connecting to the database server."""


class GoogleCloudAuthenticationError(Exception):
    """Basic class for authentication errors in Google Cloud."""


class ErrorWithGoogleCloudAuthentication(GoogleCloudAuthenticationError):
    """Authentication error in Google Cloud."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DoesNotHavePermissionForGoogleCloudSecret(
    GoogleCloudAuthenticationError
):
    """Ошибка: Недостаточно прав для доступа к Google Cloud Secret."""
