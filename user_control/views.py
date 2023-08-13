from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CreateUserSerializer, CustomUser, LoginSerializer, UpdatePasswordSerializer,
    CustomUserSerializer, UserActivities, UserActivitiesSerializer,
    InventoryActivities, InventoryActivitiesSerializer
    )
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime
from inventory_api.utils import CustomPagination, get_access_token, get_query
from inventory_api.custom_methods import IsAuthenticatedCustom


def add_user_activity(user, action):
    UserActivities.objects.create(
        user_id=user.id,
        email=user.email,
        fullname=user.fullname,
        action=action
    )


def add_inventory_activity(user, inventario, patrimonio, local, local_novo, colaborador, colaborador_novo, motivo):
    InventoryActivities.objects.create(
        user_id=user.id,
        email=user.email,
        fullname=user.fullname,
        inventario=inventario,
        patrimonio=patrimonio,
        local=local,
        local_novo=local_novo,
        colaborador=colaborador,
        colaborador_novo=colaborador_novo,
        motivo=motivo
    )


class CreateUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedCustom, )

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)

        CustomUser.objects.create(**valid_request.validated_data)

        add_user_activity(request.user, "Adicionado novo usuário")

        return Response(
            {"success": "User created successfully"},
            status=status.HTTP_201_CREATED
        )


class LoginView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)

        new_user = valid_request.validated_data["is_new_user"]

        if new_user:
            user = CustomUser.objects.filter(
                email=valid_request.validated_data["email"]
            )

            if user:
                user = user[0]
                if not user.password:
                    return Response({"user_id": user.id})
                else:
                    raise Exception("User has password already")
            else:
                raise Exception("User with email not found")

        user = authenticate(
            username=valid_request.validated_data["email"],
            password=valid_request.validated_data.get("password", None)
        )

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        access = get_access_token({"user_id": user.id}, 1)

        user.last_login = datetime.now()
        user.save()

        add_user_activity(user, "Logado em")

        return Response({"access": access})


class UpdatePasswordView(ModelViewSet):
    serializer_class = UpdatePasswordSerializer
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)

        user = CustomUser.objects.filter(
            id=valid_request.validated_data["user_id"])

        if not user:
            raise Exception("User with id not found")

        user = user[0]

        user.set_password(valid_request.validated_data["password"])
        user.save()

        add_user_activity(user, "updated password")

        return Response({"success": "User password updated"})


class MeView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )

    def list(self, request):
        data = self.serializer_class(request.user).data
        return Response(data)


class UserActivitiesView(ModelViewSet):
    serializer_class = UserActivitiesSerializer
    http_method_names = ["get"]
    queryset = UserActivities.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = CustomPagination
    
    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "fullname", "email", "action"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        return results


class InventoryActivitiesView(ModelViewSet):
    serializer_class = InventoryActivitiesSerializer
    http_method_names = ["get"]
    queryset = InventoryActivities.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = CustomPagination
    
    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        if "created_at" in data:
            try:
                created_at_date = datetime.strptime(data["created_at"], "%d/%m/%Y").date()
                data["created_at__day"] = created_at_date.day
                data["created_at__month"] = created_at_date.month
                data["created_at__year"] = created_at_date.year
            except ValueError:
                pass

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "inventario", "patrimonio", "local", "local_novo", "colaborador", 
                "colaborador_novo", "created_at",
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                results = results.filter(created_at__range=(start_date, end_date))
            except ValueError:
                pass
        
        return results


class UsersView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    pagination_class = CustomPagination
    
    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data, is_superuser=False)

        if keyword:
            search_fields = (
                "fullname", "email", "role"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        return results
