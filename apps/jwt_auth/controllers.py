from datetime import datetime
from ninja_extra import api_controller, route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt import schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainSlidingController
from ninja_jwt.tokens import SlidingToken
from apps.jwt_auth.schema import UserTokenOutSchema


@api_controller("/auth", tags=["Auth"], auth=JWTAuth())
class AuthController(TokenObtainSlidingController):
    @route.post("/login", response=UserTokenOutSchema, auth=None)
    def login(self, user_token: schema.TokenObtainSlidingInputSchema):
        user = user_token._user
        token = SlidingToken.for_user(user)

        return UserTokenOutSchema(
            token=str(token),
            user=user,
            token_exp_date=datetime.fromtimestamp(token["exp"]),
        )

    @route.post(
        "/sliding-token-refresh",
        response=schema.TokenRefreshSlidingOutputSchema,
        permissions=[IsAuthenticated])
    def refresh_token(self, refresh_token: schema.TokenRefreshSlidingInputSchema):
        refresh = schema.TokenRefreshSlidingOutputSchema(**refresh_token.dict())
        return refresh
