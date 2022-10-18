import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Group, Chat


class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('Websocket connected... ')
        print('channel_layer', self.channel_layer)
        print('channel_name', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        print(self.group_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['msg']
        if self.scope['user'].is_authenticated:
            group = Group.objects.get(name=self.group_name)
            chat = Chat(
                content=data['msg'],
                group=group
            )
            chat.save()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            self.send(text_data=json.dumps({
                'msg': 'login requered'
            }))

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'msg': event['message']
        }))

    def disconnect(self, code):
        print('Websocket Disconnected...', code)
