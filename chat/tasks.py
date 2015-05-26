from celery import shared_task
import json
import requests
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from code_stream import settings


@shared_task
def post_pastebin(username, channel, message, code, language):
    url = 'http://pastebin.com/api/api_post.php'
    params = {
        'api_dev_key': settings.PASTEBIN_ID,
        'api_paste_code': code,
        'api_option': 'paste'
    }

    if language:
        params['api_paste_format'] = language

    r = requests.post(url, params)
    print(r.content)
    if not r.content.startswith('Bad API request'):
        paste_url = r.content

        message = json.dumps({
            'user': username,
            'text': '%s\n<a href="%s">%s</a>' % (message, paste_url, paste_url)})
        RedisPublisher(facility='chat-' + channel, broadcast=True).publish_message(RedisMessage(message))