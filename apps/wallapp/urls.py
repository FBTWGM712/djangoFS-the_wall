from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('add_message', views.add_message),
    path('message/delete/<int:id>', views.delete_message),
    path('comment', views.comment),
]