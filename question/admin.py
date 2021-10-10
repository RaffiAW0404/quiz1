from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Scores)
admin.site.register(User)