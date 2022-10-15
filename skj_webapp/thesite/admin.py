from django.contrib import admin
from django.db import models
from thesite.models import Festival, Ticket, Podium, Performance, Genre, Staff

# Register your models here.
admin.site.register(Festival)
admin.site.register(Ticket)
admin.site.register(Podium)
admin.site.register(Performance)
admin.site.register(Genre)
admin.site.register(Staff)