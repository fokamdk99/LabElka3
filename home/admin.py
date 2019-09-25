from django.contrib import admin
from .models import Semestr, Przedmiot, Test, Post

# Register your models here.
admin.site.register(Semestr)
admin.site.register(Przedmiot)
admin.site.register(Test)
admin.site.register(Post)