import os

from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_selection_task.settings")

import django

django.setup()

import pytest
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from lunch_decider.models import Restaurant, Menu, Employee, Vote
from lunch_decider.serializers import (
    EmployeeSerializer,
    EmployeeListSerializer,
    EmployeeDetailSerializer,
    MenuSerializer,
    MenuDetailSerializer,
    RestaurantSerializer,
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    VoteMenuSerializer,
)


@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(
        email="testuser@example.com", password="password123"
    )
    Token.objects.create(user=user)
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def employee(user):
    return Employee.objects.create(
        user=user,
        email=user.email,
        name="Test",
        last_name="User",
        bio="Test bio",
        birth_date=date.today(),
    )


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(
        name="Test Restaurant",
        address="123 Test St",
        description="A test restaurant",
    )


@pytest.fixture
def menu(restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=date.today(),
        menu_items="Item 1\nItem 2\nItem 3",
    )


def test_employee_serializer():
    user = get_user_model().objects.create_user(
        email="testuser@example.com", password="password123"
    )
    serializer = EmployeeSerializer(data={"name": "Test", "last_name": "User", "bio": "Test bio", "user": user.id})
    assert serializer.is_valid()
    employee = serializer.save()
    assert employee.user == user


def test_employee_list_serializer(employee):
    serializer = EmployeeListSerializer(employee)
    assert serializer.data["id"] == employee.id
    assert serializer.data["full_name"] == "Test User"
    assert serializer.data["email"] == employee.email


def test_employee_detail_serializer(employee):
    serializer = EmployeeDetailSerializer(employee)
    assert serializer.data["full_name"] == "Test User"
    assert serializer.data["email"] == employee.email
    assert serializer.data["birth_date"] == date.today().isoformat()
    assert serializer.data["bio"] == "Test bio"
    assert serializer.data["profile_picture"] is None  # Assuming profile_picture is None for the created employee


def test_menu_serializer(menu):
    serializer = MenuSerializer(menu)
    assert serializer.data["menu_items"] == "Item 1\nItem 2\nItem 3"
    assert serializer.data["date"] == date.today().isoformat()


def test_menu_detail_serializer(menu):
    serializer = MenuDetailSerializer(menu)
    assert serializer.data["name"] == "Test Restaurant " + date.today().isoformat()
    assert serializer.data["total_votes"] == menu.votes.count()


def test_restaurant_serializer(restaurant):
    serializer = RestaurantSerializer(restaurant)
    assert serializer.data["name"] == "Test Restaurant"
    assert serializer.data["address"] == "123 Test St"


def test_restaurant_list_serializer(restaurant):
    serializer = RestaurantListSerializer(restaurant)
    assert serializer.data["id"] == restaurant.id
    assert serializer.data["name"] == "Test Restaurant"
    assert serializer.data["description_preview"] == "A test restaurant"


def test_restaurant_detail_serializer(restaurant):
    serializer = RestaurantDetailSerializer(restaurant)
    assert serializer.data["name"] == "Test Restaurant"
    assert serializer.data["description"] == "A test restaurant"
    assert serializer.data["address"] == "123 Test St"
    assert serializer.data["rest_picture"] is None  # Assuming rest_picture is None for the created restaurant


def test_vote_menu_serializer(menu):
    serializer = VoteMenuSerializer(menu)
    assert serializer.data["id"] == menu.id
    assert serializer.data["name"] == "Test Restaurant " + date.today().isoformat()
    assert serializer.data["total_votes"] == menu.votes.count()
