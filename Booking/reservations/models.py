from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ("conference", "Conference room"),
        ("office", "Office"),
        ("meeting room", "Meeting room"),
    ]

    name = models.CharField(max_length=200)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

def is_room_avialable(room, start, end):
    return not Booking.objects.filter(
        room=room,
        start_time__lt = end,
        end_time__gt = start,
        status__in = ['pending', 'confirmed']
    ).exists()
from django.shortcuts import render
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'reservations/room_list.html', {'rooms': rooms})

