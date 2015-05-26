import json
from celery.task import periodic_task
import datetime
import requests
from django.conf import settings
from celery import shared_task
from celery.schedules import crontab
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from stream.models import ActiveStream, Event
from users.models import UserInfo


@shared_task
def start_stream(stream_id, user_id, channel_name):
    print 'start'

    endpoint_url = 'https://api.twitch.tv/kraken/streams/%s/' % channel_name
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Accept': 'application/vnd.twitchtv.3+json'
    }
    r = requests.get(endpoint_url, headers=headers)

    stream_info = r.json()
    print(stream_info)
    if stream_info['stream']:
        UserInfo.objects.filter(user_id=user_id).update(is_streaming=True)

        active_stream = ActiveStream()
        active_stream.stream_id = stream_id
        active_stream.viewers = stream_info['stream']['viewers']
        active_stream.preview_url = stream_info['stream']['preview']['medium']
        active_stream.save()

        ws_message = json.dumps({'action': 'streams-updated', 'user': user_id})

        RedisPublisher(facility='main', broadcast=True).publish_message(RedisMessage(ws_message))


@shared_task
def update_streams():
    print 'update'

    base_url = 'https://api.twitch.tv/kraken/streams/%s/'
    headers = {
        'Client-ID': settings.TWITCH_CLIENT_ID,
        'Accept': 'application/vnd.twitchtv.3+json'
    }

    somebody_finished, streams_updated = False, False

    for active_stream in ActiveStream.objects.all():
        channel_name = active_stream.stream.owner.info.twitch_channel
        endpoint_url = base_url % channel_name

        r = requests.get(endpoint_url, headers=headers)

        stream_info = r.json()
        if stream_info['stream']:
            streams_updated = True
            active_stream.viewers = stream_info['stream']['viewers']
            active_stream.preview_url = stream_info['stream']['preview']['medium']
            active_stream.save()
        else:
            somebody_finished = True
            active_stream.stream.finished = datetime.datetime.now()
            Event.objects.create(user=active_stream.stream.owner, type=Event.STREAM_FINISHED, description='streaming.')
            active_stream.stream.save()
            active_stream.delete()

    if somebody_finished:
        somebody_finished = False
        message = json.dumps({'action': 'events-updated'})
        RedisPublisher(facility='main', broadcast=True).publish_message(RedisMessage(message))
        ws_message = json.dumps({'action': 'streams-updated'})
        RedisPublisher(facility='main', broadcast=True).publish_message(RedisMessage(ws_message))

    if streams_updated:
        streams_updated = False
        ws_message = json.dumps({'action': 'streams-updated'})
        RedisPublisher(facility='main', broadcast=True).publish_message(RedisMessage(ws_message))