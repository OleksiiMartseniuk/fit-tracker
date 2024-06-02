from src.auth.controllers import LoginController
from src.auth.services.authorization import GetActiveUser
from src.di import injector


def get_login_controller() -> LoginController:
    return injector.get(LoginController)


get_active_user = injector.get(GetActiveUser)
