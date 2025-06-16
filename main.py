from websockets.sync.client import connect
import os
import json
import time
import threading
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
    set_auto_mode,
    unset_auto_mode,
)

load_dotenv()

APP_NAME = os.environ['APP_NAME']
websocket_server_url = "ws://5.133.9.244:10001"
exit_flag = threading.Event()

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
    elif message == 'admit': # Admit is not supported yet
        admit_user()
    elif message == 'switchtab': # only works on macos
        switch_tab()
    elif message == 'switch':
        switch_window()
    elif message == 'focus':
        focus_zoom_meeting()
    elif message == 'hide':
        hide_window()
    elif message == 'autoon':
        set_auto_mode()
    elif message == 'autooff':
        unset_auto_mode()

def send_ping(ws):
    while not exit_flag.is_set():
        try:
            ws.send("ping")
        except Exception as e:
            print("Ping failed:", e)
            exit_flag.set()  # Signal the main loop to exit
            return
        time.sleep(30)  # Send ping every 30 seconds

if __name__ == "__main__":
    while True:
        try:
            with connect(websocket_server_url) as ws:
                ws.send(json.dumps({"room": APP_NAME, "type": "join"}))
                print('Opened connection')

                # Start a background thread for pinging
                exit_flag.clear()
                ping_thread = threading.Thread(target=send_ping, args=(ws,), daemon=True)
                ping_thread.start()

                while not exit_flag.is_set():
                    try:
                        message = ws.recv(timeout=60)
                        if message:
                            on_message(message)
                            print(f"Received: {message}")
                    except TimeoutError:
                        continue  # Allow checking of exit_flag
                    except Exception as e:
                        print("WebSocket error:", e)
                        exit_flag.set()
        except Exception as e:
            print('Connection error:', e)

        time.sleep(5)  # Wait before reconnecting
