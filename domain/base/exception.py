from dataclasses import dataclass


@dataclass(eq=False)
class BaseApplicationException(Exception):
    message: str


class BaseServiceException(BaseApplicationException):
    pass


class BaseRepositoryException(BaseApplicationException):
    pass
