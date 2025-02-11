class ErrorWithGoogleCloudAuthentication(Exception):
    def __init__(self, message: str):
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
