from websockets.sync.client import connect
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
websocket_server_url = "ws://5.133.9.244:10010"

def on_message(message):
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

def send_ping(ws):
    while True:
        try:
            ws.send("ping")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(30)  # Send ping every 30 seconds


if __name__ == "__main__":
    while True:
        try:

            with connect(websocket_server_url) as ws:
                ws.send(json.dumps({"room": APP_NAME, "type": "join"}))
                print('Opened connection')

                # Start a background thread for pinging
                ping_thread = threading.Thread(target=send_ping, args=(ws,), daemon=True)
                ping_thread.start()

                while True:
                    message = ws.recv()
                    on_message(message)
                    print(f"Received: {message}")
        except Exception as e:
            print('ERR', e)
        time.sleep(10)