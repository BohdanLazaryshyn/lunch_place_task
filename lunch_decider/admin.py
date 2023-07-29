from django.contrib import admin

from lunch_decider.models import Restaurant, Menu, Employee, Vote

admin.site.register(Employee)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Vote)

