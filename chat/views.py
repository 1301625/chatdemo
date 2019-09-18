import json     #삭제

from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from .models import Post,Message


def index(request):
    post = Post.objects.all()
    return render(request, 'chat/index.html', {"posts": post})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'chat/detail.html', {'post': post})


# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#
#     })
#def chat(request):
#    return render(request, '' ,{})

# def room(request, room_name, pk):
#     chat_message = get_object_or_404(Message, pk)
#     #chat_message = Message.objects.order_by('created').all()[:100]
#     return render(request, 'chat/room.html',{
#         'chat_messages': chat_message,
#         'room_name' : room_name
#     })

def room(request, pk):
    chat_message = Message.objects.filter(post_id=pk)
    #chat_message = Message.objects.order_by('created').all()[:100]
    return render(request, 'chat/room.html',{
        'chat_messages': chat_message,
        'pk' : pk
    })
