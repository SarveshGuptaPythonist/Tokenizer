from django.contrib import admin
from django.urls import path
from . import views
from vendor import views

urlpatterns = [
    path('contact/', views.contact, name="contact"),
    path('roc/<int:tokhen>/<int:choice>', views.roc, name = 'roc'),
    path('', views.loginpage, name="vendorpage"),
    path('login/', views.loginpage, name="login"),
    path('signup/', views.signuppage, name="signup"),
    path('dashBoard/', views.dashBoard,name="dashboard"),
    path('trackToken/', views.trackToken,name="trackToken"),
    path('signuprequest/', views.handleSignUp, name="handleSignUp"),
    path('loginrequest/', views.handelLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
]
