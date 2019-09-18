import json
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import Message


def index(request):
    return render(request, 'chat/index.html', {})


# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#
#     })


def room(request, room_name):
    chat_message = Message.objects.order_by('created').all()[:100]
    return render(request, 'chat/room.html',{
        'chat_messages': chat_message,
        'room_name' : room_name
    })

