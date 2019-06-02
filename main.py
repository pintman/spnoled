import websocket  # pip install websocket_client https://pypi.org/project/websocket_client/
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import schlangen_websocket as sws
from bots import Bot
import display
import sys

url = sws.url

all_bots = []
num_msgs = 0
JOYSTICK_MOVEMENT = 1  # Pixel per joystick event
SLEEP_AFTER_UPDATE = 0.05 # Seconds
USE_JOYSTICK = True
SEND_TO_PROCESSING = True

if SEND_TO_PROCESSING:
    oled_display = display.ProcessingAdditionalDisplay()
else:
    oled_display = display.Display()


def on_message(ws, message):
    global num_msgs
    num_msgs += 1
    msg_json = json.loads(message)

    if sws.is_bot_moved_head(msg_json):
        handle_bot_moved_head(msg_json['items'])

def handle_bot_moved_head(bots_list):
    maxx, maxy = 0, 0    
    all_bots.clear()
    oled_display.clear()
    bots_in_display = 0
    for bot_json in bots_list:
        b = Bot(bot_json, oled_display)
        if b.on_display():
            bots_in_display += 1
        #print("bot created ", b)
        all_bots.append(b)
        b.draw()

        maxx, maxy = max(maxx, b.pos[0]), max(maxy, b.pos[1])

    oled_display.update()
    time.sleep(SLEEP_AFTER_UPDATE)
    print("#" + str(num_msgs), "botscount", len(bots_list), 
          "on_display", bots_in_display, "maxxy", round(maxx, 2), round(maxy, 2))


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("opened")
    def run(*args):
        auth = '{"viewer_key": ' + sws.viewer_key + '}'
        #print("send auth", auth)
        ws.send(auth)
        time.sleep(1)
        #ws.close()
        #print("thread finished...")
        
    thread.start_new_thread(run, ())

def joystick_handling():
    print("Started Joystick handling")
    while True:
        byte_input = oled_display.ser.read(1)[0]
        handle_joystick_event(byte_input)


def handle_joystick_event(joystick_event):
    print("Handling Joystick event", joystick_event) #, chr(joystick_event))

    if joystick_event == ord('w'):
        oled_display.offset[1] -= JOYSTICK_MOVEMENT
    elif joystick_event == ord('a'):
        oled_display.offset[0] -= JOYSTICK_MOVEMENT
    elif joystick_event == ord('s'):
        oled_display.offset[1] += JOYSTICK_MOVEMENT
    elif joystick_event == ord('d'):
        oled_display.offset[0] += JOYSTICK_MOVEMENT
    elif joystick_event == ord('e'):
        print("Joystick button pressed")

    print("Display offset", oled_display.offset)

def main():
    websocket.enableTrace(True)
    print("connecting to", url)
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    if USE_JOYSTICK:
        thread.start_new_thread(joystick_handling, ())
    ws.run_forever()


if __name__ == "__main__":
    main()
