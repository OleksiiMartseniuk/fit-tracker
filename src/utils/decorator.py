import functools
import logging
import re

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.exceptions import BaseRepositoryException

__all__ = ["error_handler_sqlalchemy"]

logger = logging.getLogger(__name__)


def _extract_error_details(error_message: str) -> str:
    match = re.search(r"DETAIL:  (.+?)\n", error_message)
    if match:
        return match.group(1)
    return error_message


def error_handler_sqlalchemy(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            msg = f"Database error. {_extract_error_details(str(e))}"
            logger.error(msg, exc_info=e)
            raise BaseRepositoryException(message=msg)
        except IntegrityError as e:
            msg = f"Data integrity error. {_extract_error_details(str(e))}"
            logger.error(msg, exc_info=e)
            raise BaseRepositoryException(message=msg)

    return wrapper
