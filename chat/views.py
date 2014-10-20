from rest_framework.decorators import api_view
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from pygments import highlight
from pygments.lexers import PythonLexer, guess_lexer
from pygments.formatters import HtmlFormatter

from chat.serializers import MessageSerializer


redis_publisher = RedisPublisher(facility='foobar', broadcast=True)


@api_view(['POST'])
def post(request):
    srlzr = MessageSerializer(data=request.DATA)
    if srlzr.is_valid():
        parsed_message = srlzr.data
        highlighted_message = highlight(parsed_message['text'], PythonLexer(), HtmlFormatter(linenos=True))
        redis_publisher.publish_message(RedisMessage(highlighted_message))
        return Response(highlight(parsed_message['text'], PythonLexer(), HtmlFormatter()))
    else:
        return Response(srlzr.errors)