from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # where room.topic.name includes q; icontains - case insensitive, if q='', will return all
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))
    topics = Topic.objects.all()

    # pass data to template
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)  # incoming data from form

        if form.is_valid():
            form.save()  # saves data to db (room table)
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)  # find room
    form = RoomForm(instance=room)  # form will be prefilled with room values

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})
