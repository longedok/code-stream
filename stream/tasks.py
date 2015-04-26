import requests
from django.conf import settings
from celery import shared_task
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from stream.models import ActiveStream


redis_publisher = RedisPublisher(facility='streams', broadcast=True)


@shared_task
def start_stream(stream_id, channel_name):
    endpoint_url = 'https://api.twitch.tv/kraken/streams/%s/' % channel_name
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Accept': 'application/vnd.twitchtv.3+json'
    }
    r = requests.get(endpoint_url, headers=headers)

    stream_info = r.json()
    print(stream_info)
    if stream_info['stream']:
        active_stream = ActiveStream()
        active_stream.stream_id = stream_id
        active_stream.save()
        redis_publisher.publish_message(RedisMessage('streams.started'))