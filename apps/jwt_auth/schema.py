from datetime import datetime
from ninja_schema import Schema, ModelSchema
from ..users.models import User


class UserTokenSchema(ModelSchema):
    class Config:
        model = User
        include = ['id', 'username', 'email']


class UserTokenOutSchema(Schema):
    token: str
    user: UserTokenSchema
    token_exp_date: datetime | None
