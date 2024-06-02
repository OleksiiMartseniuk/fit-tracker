from fastapi import FastAPI

from src.api.v1.account.router import router as account_router
from src.api.v1.auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/v1")
app.include_router(account_router, prefix="/v1")
