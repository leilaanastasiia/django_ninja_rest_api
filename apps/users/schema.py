from typing import Type
from django.contrib.auth.models import AbstractUser
from ninja_extra import status
from ninja_extra.exceptions import APIException
from ninja_schema import Schema, ModelSchema
from pydantic import field_validator
from .models import User


class UserCreateSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'password', 'email', 'first_name', 'last_name']

    @field_validator('username')
    def validate_unique_username(cls, value: str) -> str:
        if User.objects.filter(username__iexact=value).exists():
            exception = APIException("Username is already taken")
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception
        return value

    @field_validator('email')
    def validate_unique_email(cls, email: str) -> str:
        if User.objects.filter(email__iexact=email).exists():
            exception = APIException("Email is already taken")
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception
        return email

    def create_user(self) -> Type[AbstractUser]:
        return User.objects.create_user(**self.dict())


class UserInSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'password', 'email', 'first_name', 'last_name']


class UserOutSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


class UserGenericSchema(Schema):
    id: int
    _user: None

    @field_validator("id")
    def validate_user_id(cls, value: int) -> int:
        try:
            user = User.objects.filter(id=value).get()
            cls._user = user
            return value
        except User.DoesNotExist:
            exception = APIException("No user with this ID exists")
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception

    def get_user(self) -> Type[AbstractUser]:
        return self._user

    def update_user(self, data: UserInSchema):
        for attribute, value in data.dict().items():
            setattr(self._user, attribute, value)
        self._user.save()
        return self._user

    def delete_user(self):
        _id = self._user.pk
        self._user.delete()
        return _id


class MessageSchema(Schema):
    message: str


class ErrorSchema(Schema):
    error: str
