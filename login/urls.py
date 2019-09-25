from django.urls import path

from . import views
from home.views import index

urlpatterns = [
    path('', index, name="index"),
    path('log_in', views.log_in, name="log_in"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('login_authenticate', views.login_authenticate, name="login_authenticate"),
    path('create_new_user', views.create_new_user, name="create_new_user"),
    path('log_out', views.log_out, name="log_out"),
]