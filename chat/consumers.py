
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from .models import Message

import json
import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #self.room_name = self.scope['url_route']['kwargs']['pk'] #chat/routing.py에 정의된 URL 파라미터에서 room_name을 얻습니다.
        #self.room_group_name = 'chat_%s' % self.room_name #사용자가 지정한 방 이름에서 직접 채널 그룹 이름을 구축합니다.
        self.room_group_name = self.scope['url_route']['kwargs']['pk']

        #그룹에 join(결합)합니다.
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.accept() # 웹 소켓 연결 허용

    def disconnect(self, code):
        #그룹을 떠납니다
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        user = str(self.scope['user'])
        pk = self.scope['url_route']['kwargs']['pk']
        now_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)

        if not message:
            return
        if not self.scope['user'].is_authenticated:
            return

        Message.objects.create(user=self.scope['user'], message=message, post_id=pk)

        #그룹에게 이벤트를 보냅니다.
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message', #이벤트는 특별이 'type'이벤트를받을 소비자 호출하는 메소드의 이름에 해당하는 키를 누릅니다
                'message': message,
                'user':user,
                'now_time':now_time
            }
        )


    def chat_message(self, event):
        message = event['message']
        now_time = event['now_time']
        user = event['user']

        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time
        }))