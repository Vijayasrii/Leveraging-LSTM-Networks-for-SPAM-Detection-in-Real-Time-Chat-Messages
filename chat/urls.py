from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),  # Place logout before room
    path('home/', views.home, name='home'),
    path('home/checkview', views.checkview, name='checkview'),
    path('<str:room>/', views.room, name='room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('admin-login', views.AdminLogin, name='admin-login'),
    path('view-users', views.ViewUsersPage, name='view-users'),
    path('admin-home', views.AdminHomePage, name='admin-home'),
    path('base/', views.base, name='base'),
    path('user-activate/<int:pk>/', views.UserActivateFunction, name='user-activate'),   # ✅ for Activate
    path('user-deactivate/<int:pk>/', views.UserDeactivateFunction, name='user-deactivate'),
    path('user-delete/<int:pk>/', views.UserDeleteFunction, name='user-delete'),   # ✅ for Delete

]
