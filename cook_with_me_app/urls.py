from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.loginPage),
    path('register', views.register),
    path('login_now', views.login),
    path('logout', views.logout),
    path('bookings', views.bookings),
    path('restaurant/new', views.newRestaurant),
    path('restaurant/new/create', views.restaurantCreate),
    path('restaurant/<int:course_id>', views.restaurant),
    # path('restaurant/<int:course_id>/edit', views.restaurantEditPage),
]