import traceback
from ninja import Form
from ninja_extra import status, api_controller, ControllerBase, route, paginate
from ninja_extra.exceptions import APIException
from ninja_extra.pagination import PageNumberPaginationExtra
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
from ninja_extra.schemas import PaginatedResponseSchema
from ninja_jwt.authentication import JWTAuth
from .models import User
from .schema import UserOutSchema, UserGenericSchema, UserCreateSchema, MessageSchema, UserInSchema


@api_controller('/users', tags=['Users'], auth=JWTAuth())
class UserController(ControllerBase):
    @route.post('signup/', response={201: UserOutSchema}, auth=None)
    def signup(self, data: Form[UserCreateSchema]):
        try:
            user = data.create_user()
            return 201, user
        except Exception as err:
            exception = APIException(''.join(traceback.format_exception_only(err)).strip())
            exception.status_code = status.HTTP_400_BAD_REQUEST
            raise exception

    @route.get(
        '',
        response={200: PaginatedResponseSchema[UserOutSchema]},
        permissions=[IsAuthenticated,]
    )
    @paginate(PageNumberPaginationExtra, page_size=20)
    def get_users(self):
        return User.objects.all()

    @route.get(
        '{int:pk}',
        response={200: UserOutSchema},
        permissions=[IsAuthenticated,]
    )
    def get_user(self, pk: int):
        user = UserGenericSchema(id=pk)
        return user.get_user()

    @route.delete(
        'delete/{int:pk}',
        response={200: MessageSchema},
        permissions=[IsAuthenticated, IsAdminUser],
    )
    def delete_user(self, pk: int):
        user = UserGenericSchema(id=pk)
        user.delete_user()
        return self.create_response('User has been deleted', status_code=status.HTTP_200_OK)

    @route.put(
        'update/{int:pk}',
        response={200: UserOutSchema},
        permissions=[IsAuthenticated],
    )
    def update_user(self, pk: int, data: Form[UserInSchema]):
        user = UserGenericSchema(id=pk)
        return user.update_user(data)
