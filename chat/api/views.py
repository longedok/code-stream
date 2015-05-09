import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from chat.api.serializers import MessageSerializer


@api_view(['POST'])
def post(request, username):
    serializer = MessageSerializer(data=request.DATA)
    if serializer.is_valid(raise_exception=True) and request.user.is_authenticated():
        parsed_message = serializer.validated_data
        is_code = parsed_message.get('code', False)

        if is_code:
            message_content = highlight(parsed_message['text'], PythonLexer(), HtmlFormatter(linenos=False))
        else:
            message_content = parsed_message['text']

        message = json.dumps({'user': request.user.username, 'text': message_content})
        RedisPublisher(facility='chat-' + username, broadcast=True).publish_message(RedisMessage(message))
        return Response('', status=status.HTTP_200_OK)
    else:
        return Response('', status=status.HTTP_403_FORBIDDEN)