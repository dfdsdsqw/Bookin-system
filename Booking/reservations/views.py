from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from reservations.form import BookingForm
from reservations.models import is_room_avialable
from .models import Room, Booking
from django.contrib.auth.decorators import login_required

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'reservations/room_list.html', {'rooms': rooms})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'reservations/booking_list.html', {'bookings': bookings})

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            if is_room_available(
                booking.room,
                booking.start_time,
                booking.end_time
            ):
                booking.save()
                messages.success(request, "Booking created!")
                return  redirect('room_list')
            else:
                messages.error(request, "Room not available!")
    else:
        form = BookingForm()
    return render(request, 'reservations/booking_form.html', {'form': form})


