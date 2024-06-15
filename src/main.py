import logging
import logging.config

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.api.v1.account.router import router as account_router
from src.api.v1.auth.router import router as auth_router
from src.config import LOGGING_CONFIG
from src.exceptions import BaseApplicationException

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

app.include_router(auth_router, prefix="/v1")
app.include_router(account_router, prefix="/v1")


@app.exception_handler(BaseApplicationException)
async def base_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )
