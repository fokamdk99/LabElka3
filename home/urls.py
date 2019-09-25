from django.urls import path

from . import views

urlpatterns = [
    path('upload_post/<str:przedmiot>/<str:test>', views.upload_post, name="upload_post"),
    path('semestr/<int:number>/', views.semester, name="semester_content"),
    path('semestr/<int:number>/<slug:nazwa>/', views.przedmiot, name = "przedmiot_content"),
    path('semestr/<int:number>/<slug:nazwa>/<slug:test>/', views.posts, name = "posts_content"),
    path('add_post', views.upload_post1, name='add_post')
]