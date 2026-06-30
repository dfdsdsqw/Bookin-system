from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name="room_list"),
    path('book', views.create_booking, name="create_booking"),
    path('booking', views.booking_list, name="booking_list"),
]