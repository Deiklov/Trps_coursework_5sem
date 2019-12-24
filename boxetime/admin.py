from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(Competition)
admin.site.register(AddRequest)
admin.site.register(CompetitGrid)
admin.site.register(Profile)
