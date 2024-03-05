from ninja import Schema


class MassageError(Schema):
    status_code: int
    detail: str
