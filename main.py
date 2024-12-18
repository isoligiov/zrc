import websocket
import ssl
import rel
import os
import json
from dotenv import load_dotenv
import time
from zoomer import (
  open_zoom_app,
  create_zoom_room,
  approve_remote_control,
  press_enter,
  share_screen,
  admit_user,
  switch_tab,
  switch_window,
  focus_zoom_meeting,
  hide_window,
)

load_dotenv()

APP_NAME = os.environ['APP_NAME']

def on_message(ws, message):
    if message == 'open':
        open_zoom_app()
    elif message == 'create':
        create_zoom_room()
    elif message == 'approve' or message == "accept":
        approve_remote_control()
    elif message == 'enter':
        press_enter()
    elif message == 'share':
        share_screen()
    elif message == 'admit':
        admit_user()
    elif message == 'switchtab':
        switch_tab()
    elif message == 'switch':
        switch_window()
    elif message == 'focus':
        focus_zoom_meeting()
    elif message == 'hide':
        hide_window()

def on_error(ws, error):
    print(error)
    time.sleep(5)
    reconnect()

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    time.sleep(5)
    reconnect()

def on_open(ws):
    print("Opened connection")
    ws.send_text(json.dumps({"room": APP_NAME, "type": "join"}))

def reconnect():
    ws = websocket.WebSocketApp(f"wss://streamlineanalytics.net:10001",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, dispatcher=rel, reconnect=5)

if __name__ == "__main__":
    websocket.enableTrace(True)
    reconnect()
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()