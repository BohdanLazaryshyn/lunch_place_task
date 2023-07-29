import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_selection_task.settings")

import django

django.setup()
import pytest

from django.contrib.auth import get_user_model

from lunch_decider.models import Employee, Restaurant, Menu, Vote


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        email="testuser@example.com", password="password123"
    )

@pytest.fixture
def employee(user):
    return Employee.objects.create(
        user=user,
        email=user.email,
        name="Test",
        last_name="User",
        bio="Test bio",
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
        menu_items="Item 1\nItem 2\nItem 3",
    )

@pytest.fixture
def vote(employee, menu):
    return Vote.objects.create(user=employee, menu=menu)

@pytest.mark.django_db
def test_employee_model(employee):
    assert isinstance(employee, Employee)
    assert employee.full_name == "Test User"
    assert str(employee) == "Test User - testuser@example.com"

@pytest.mark.django_db
def test_restaurant_model(restaurant):
    assert isinstance(restaurant, Restaurant)
    assert str(restaurant) == "Test Restaurant"

@pytest.mark.django_db
def test_menu_model(menu):
    assert isinstance(menu, Menu)
    assert menu.total_votes == 0
    assert str(menu) == "Test Restaurant " + str(menu.date)

@pytest.mark.django_db
def test_vote_model(vote):
    assert isinstance(vote, Vote)
    assert str(vote) == "Test User voted for Test Restaurant " + str(vote.menu.date)
