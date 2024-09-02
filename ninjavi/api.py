from ninja_extra import NinjaExtraAPI
from apps.jwt_auth.controllers import AuthController
from apps.users.controllers import UserController


api = NinjaExtraAPI(csrf=True)
api.register_controllers(UserController, AuthController)
