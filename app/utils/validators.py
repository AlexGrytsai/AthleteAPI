import logging
from typing import Union

logger = logging.getLogger(__name__)


class DBParamValidator:
    @staticmethod
    def validate_parameter_from_secret(
        param: str,
        value: Union[str, int, None],
    ) -> str:
        if isinstance(value, str):
            return value

        error_message = (
            f"Invalid type for database parameter '{param}'. "
            f"Value '{value}' has type '{type(value).__name__}'. "
            f"Allowed types: String."
        )
        logger.error(error_message)
        raise TypeError(error_message)
