import json
import re
from django.contrib.auth.models import User
from pygments.util import ClassNotFound
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

from chat.api.serializers import MessageSerializer
from chat.tasks import post_pastebin


regexp = r'/(\w+)(?:=(\w+))?'
pattern = re.compile(regexp, flags=re.S)


def parse_message(text):
    """
    :param text:
    :return: (command, parameter, message, code) if a command was found, None otherwise
    """
    match = pattern.search(text)
    if match:
        message = text[:match.start()].strip()
        code = text[match.end():].strip()
        command, parameter = match.group(1), match.group(2)
        return command.lower(), parameter.lower(), message, code


def highlight_code(code, language=None):
    if language:
        try:
            lexer = get_lexer_by_name(language.strip())
        except ClassNotFound:
            lexer = guess_lexer(code)
    else:
        lexer = guess_lexer(code)

    return highlight(code.strip(), lexer, HtmlFormatter(linenos=False))


@api_view(['POST'])
def post(request, username):
    serializer = MessageSerializer(data=request.DATA)
    if serializer.is_valid(raise_exception=True) and request.user.is_authenticated():
        text = serializer.validated_data['text']

        parsed_message = parse_message(text)
        if parsed_message:
            command, language, message, code = parsed_message
            if command == 'code':
                result_text = '%s\n%s' % (message, highlight_code(code, language))
            elif command == 'paste':
                post_pastebin.delay(request.user.username, username, message, code, language)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response('Unknown command', status=status.HTTP_400_BAD_REQUEST)
        else:
            result_text = text

        message = json.dumps({'user': request.user.username, 'text': result_text})
        RedisPublisher(facility='chat-' + username, broadcast=True).publish_message(RedisMessage(message))
        return Response(status=status.HTTP_200_OK)
    else:
        return Response('', status=status.HTTP_403_FORBIDDEN)