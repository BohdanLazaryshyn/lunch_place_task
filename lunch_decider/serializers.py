from datetime import date

from rest_framework import serializers

from lunch_decider.models import Restaurant, Menu, Employee, Vote


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "email"]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "full_name",
            "email",
            "birth_date",
            "bio",
            "profile_picture",
        ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "name",
            "menu_items",
            "today_menu",
            "total_votes",
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "description_preview"]


class RestaurantDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "description",
            "address",
            "rest_picture",
        ]


class VoteSerializerV1(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(date=date.today())
    )

    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        menu = validated_data.get("menu")
        request = self.context["request"]

        # We are checking if the user has already voted 2 times for this menu.
        user = request.user.employee
        if Vote.objects.filter(user=user, menu=menu).count() >= 2:
            raise serializers.ValidationError(
                "You have reached the maximum number of votes for this menu."
            )

        validated_data["user"] = user
        return super().create(validated_data)


class VoteSerializerV2(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(date=date.today())
    )

    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        menu = validated_data.get("menu")
        request = self.context["request"]

        # We are checking if the user has already voted for this menu.
        user = request.user.employee
        if Vote.objects.filter(user=user, menu=menu).exists():
            raise serializers.ValidationError(
                "You have already voted for this menu."
            )

        validated_data["user"] = user
        return super().create(validated_data)


class VoteMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "total_votes"]
        ordering = ["total_votes"]
