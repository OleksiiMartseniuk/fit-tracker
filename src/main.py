import logging.config

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqladmin import Admin

from src.account.admin import UserAdmin
from src.api.v1.account.router import router as account_router
from src.api.v1.auth.router import router as auth_router
from src.auth.admin import TokenAdmin
from src.auth.services.admin import authentication_backend
from src.config import LOGGING_CONFIG
from src.database.base import engine_async
from src.exceptions import BaseApplicationException

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()
admin = Admin(
    app=app,
    engine=engine_async,
    authentication_backend=authentication_backend,
)

# Register routers
app.include_router(auth_router, prefix="/v1")
app.include_router(account_router, prefix="/v1")

# Register admin views
admin.add_view(UserAdmin)
admin.add_view(TokenAdmin)


@app.exception_handler(BaseApplicationException)
async def base_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )
