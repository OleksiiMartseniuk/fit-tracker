from dataclasses import dataclass


@dataclass(eq=False)
class BaseApplicationException(Exception):
    message: str
