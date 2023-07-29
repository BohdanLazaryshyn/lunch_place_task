from django.urls import path, include
from rest_framework import routers

from lunch_decider.views import (
    RestaurantViewSet,
    MenuViewSet,
    EmployeeViewView, VoteView, TodayMenuView, TopMenuView
)

app_name = "lunch_decider"

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet)
router.register("employees", EmployeeViewView)

urlpatterns = [
    path("", include(router.urls)),
    path("votes/", VoteView.as_view(), name="create-vote"),
    path("today/", TodayMenuView.as_view(), name="today-menu"),
    path("top/", TopMenuView.as_view(), name="top-menu"),
]
