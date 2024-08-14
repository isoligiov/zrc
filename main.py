import websocket
import rel
import os
from dotenv import load_dotenv
from zoomer import create_zoom_room

load_dotenv()

REMOTE_COMMAND_WSS_HOST = os.environ['REMOTE_COMMAND_WSS_HOST']
REMOTE_COMMAND_WSS_PORT = os.environ['REMOTE_COMMAND_WSS_PORT']

def on_message(ws, message):
    if message == 'create_room':
        create_zoom_room()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send_text('zoom')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://{REMOTE_COMMAND_WSS_HOST}:{REMOTE_COMMAND_WSS_PORT}",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()