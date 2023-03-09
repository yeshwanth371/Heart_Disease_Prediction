from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home1,name='home1'),
    path('signup',views.signup,name = "signup"),
    path('signin',views.signin,name = "signin"),
    path('signout',views.signout,name = "signout"),
    path('home',views.home,name = "home"),
    path('predict',views.predict,name = "predict"),
]