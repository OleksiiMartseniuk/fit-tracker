from src.account.controllers import UserController
from src.di import injector


def get_user_controller() -> UserController:
    return injector.get(UserController)
