from django.contrib.auth.models import User
from rest_framework import mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from django_base.filters.user_list_query import apply_user_list_query_params
from django_base.serializers.user import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)

F = TypeVar("F", bound=Callable[..., Any])

if TYPE_CHECKING:

    def profile(func: F) -> F: ...

else:
    try:
        profile
    except NameError:

        def profile(func: F) -> F:
            return func


class UserPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class UserController(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all().order_by("id")
    pagination_class = UserPagination

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action in ("update", "partial_update"):
            return UserUpdateSerializer
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserListSerializer

    @profile
    def list(self, request, *args, **kwargs):
        queryset = apply_user_list_query_params(
            self.get_queryset(), request.query_params
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        paginator = self.paginator
        return Response(
            {
                "data": {
                    "results": serializer.data,
                    "pagination": {
                        "page": paginator.page.number,
                        "page_size": paginator.get_page_size(request),
                        "total": paginator.page.paginator.count,
                    },
                }
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({"data": response.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"data": {"id": user.id, "username": user.username, "email": user.email}},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"data": response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
