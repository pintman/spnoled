url = 'wss://schlangen.bytewerk.org:443/websocket'
viewer_key = '4946823228349712590'

def get_topic(json_msg):
    return json_msg['t']

def is_world_update(msg_json):
    return get_topic(msg_json) == 'WorldUpdate'

def is_bot_moved_head(msg_json):
    return get_topic(msg_json) == 'BotMoveHead'
