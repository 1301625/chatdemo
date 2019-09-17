from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

#클라이언트와 Channels 개발 서버가 연결 될 때, 어느 protocol 타입의 연결인지
application = ProtocolTypeRouter({
    #만약에 websocket protocol 이라면, AuthMiddlewareStack
    # URLRouter 로 연결, 소비자의 라우트 연결 HTTP path를 조사
    'websocket': AuthMiddlewareStack(
        URLRouter(

            chat.routing.websocket_urlpatterns
        )
    ),
})