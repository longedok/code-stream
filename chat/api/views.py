from rest_framework.decorators import api_view
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from chat.api.serializers import MessageSerializer


redis_publisher = RedisPublisher(facility='chat', broadcast=True)


@api_view(['POST'])
def post(request):
    serializer = MessageSerializer(data=request.DATA)
    if serializer.is_valid(raise_exception=True):
        parsed_message = serializer.data
        highlighted_message = highlight(parsed_message['text'], PythonLexer(), HtmlFormatter(linenos=True))
        redis_publisher.publish_message(RedisMessage(highlighted_message))
        return Response(highlight(parsed_message['text'], PythonLexer(), HtmlFormatter()))