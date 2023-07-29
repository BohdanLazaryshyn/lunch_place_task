import datetime

from rest_framework import viewsets, status, generics, versioning
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from lunch_decider.models import Restaurant, Menu, Employee, Vote
from lunch_decider.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from lunch_decider.serializers import (
    RestaurantSerializer,
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    MenuDetailSerializer,
    MenuSerializer,
    VoteMenuSerializer,
    EmployeeSerializer,
    EmployeeListSerializer,
    EmployeeDetailSerializer,
    VoteSerializerV2,
    VoteSerializerV1
)


class EmployeeViewView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        if self.action == "retrieve":
            return EmployeeDetailSerializer
        return EmployeeSerializer

    def create(self, request, *args, **kwargs):
        if Employee.objects.filter(user=request.user).exists():
            return Response(
                {"error": "You already have an employee profile."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantListSerializer
        if self.action == "retrieve":
            return RestaurantDetailSerializer
        return RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(date=datetime.date.today())
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return VoteMenuSerializer
        if self.action == "retrieve":
            return MenuDetailSerializer
        return MenuSerializer


class TodayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = datetime.date.today()
        return Menu.objects.filter(date=today)


class VoteView(generics.CreateAPIView):
    versioning_class = versioning.AcceptHeaderVersioning
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        version = self.request.version
        if version == "1.0":
            return VoteSerializerV1
        elif version == "2.0":
            return VoteSerializerV2

        return VoteSerializerV2

    def get_queryset(self):
        return Vote.objects.none()

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TopMenuView(generics.ListAPIView):
    serializer_class = MenuDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = datetime.date.today()
        return Menu.objects.filter(date=today).order_by("-votes")[:1]
