from pyautogui import press, hotkey, click
from utils import (
  bring_zoom_window_to_top,
  zoom_window_exists,
  hide_zoom_window,
  find_text_in_screen,
  move_mouse_smoothly,
  vpn_connected,
)
import time
import os
import subprocess
import sys
from config import ZOOM_APP_WINDOWS_PATH
import threading

def open_zoom_app():
  if sys.platform == "darwin":
    os.system("open /Applications/zoom.us.app")
  elif sys.platform == "win32":
    subprocess.Popen(ZOOM_APP_WINDOWS_PATH)

def create_zoom_room():
  # check if zoom meeting is already created
  zoom_meeting_found = zoom_window_exists("Zoom Meeting")
  if zoom_meeting_found == 'yes':
    return

  # focus zoom main window
  bring_zoom_window_to_top("Zoom Workplace")
  time.sleep(1)

  # trigger zoom room create
  zoom_meeting_found = 'no'
  for i in range(3):
    if sys.platform == "darwin":
      hotkey('command', 'ctrl', 'v')
    elif sys.platform == "win32":
      hotkey('alt', 'ctrl', 'v')
    
    time.sleep(3)
    zoom_meeting_found = zoom_window_exists("Zoom Meeting")
    if zoom_meeting_found == 'yes':
      break
  
  # check if zoom room is created
  if zoom_meeting_found == 'no':
    return False

  time.sleep(7)
  
  # Share screen
  time.sleep(1)
  share_screen()

def approve_remote_control():
  time.sleep(1)
  approve_position = find_text_in_screen('Approve', 400)
  if approve_position is not None:
    x, y = approve_position
    move_mouse_smoothly(x, y, duration=0.5)
    click(x, y)

  time.sleep(0.5)
  confirm_position = find_text_in_screen('Confirm', 300)
  if confirm_position is not None:
    x, y = confirm_position
    move_mouse_smoothly(x, y, duration=0.5)
    click(x, y)


def share_screen():
  bring_zoom_window_to_top("Zoom Meeting")
  time.sleep(1)
  if sys.platform == "darwin":
    hotkey('command', 'shift', 's')
  elif sys.platform == "win32":
    hotkey('alt', 'shift', 's')
  time.sleep(5)

def admit_user():
  bring_zoom_window_to_top("Zoom Meeting")
  admit_position = find_text_in_screen('Admit', 200)
  if admit_position is None:
    print('Admit button not found')
    return
  x, y = admit_position
  move_mouse_smoothly(x, y, duration=0.5)
  click(x, y)

def focus_zoom_meeting():
  bring_zoom_window_to_top("Zoom Meeting")

def press_enter():
  press('enter')

def switch_tab():
  if sys.platform == "darwin":
    hotkey('command', '`')

def switch_window():
  if sys.platform == "darwin":
    hotkey('command', 'tab')
  elif sys.platform == "win32":
    hotkey('alt', 'tab')

def hide_window():
  hide_zoom_window()



auto_mode_thread_instance = None
auto_mode_stop_event = threading.Event()

def auto_mode_thread():
    print('auto mode thread started')
    while not auto_mode_stop_event.is_set():
        connected = vpn_connected()
        if connected:
            break
        time.sleep(1)

    print('auto mode set')

    while not auto_mode_stop_event.is_set():
        zoom_meeting_found = zoom_window_exists("Zoom Meeting")
        zoom_floating_found = zoom_window_exists("floating")
        print(zoom_meeting_found, zoom_floating_found)
        if zoom_meeting_found == 'no' and zoom_floating_found == 'no':
            create_zoom_room()
            time.sleep(2)
            continue

        control_window_found = zoom_window_exists("missing")
        print("control_window_found", control_window_found)
        if control_window_found == 'yes':
            approve_remote_control()
        time.sleep(2)

def set_auto_mode():
    print('setting auto mode')
    global auto_mode_thread_instance
    
    if auto_mode_thread_instance is not None:
        return
        
    auto_mode_stop_event.clear()
    auto_mode_thread_instance = threading.Thread(target=auto_mode_thread, daemon=True)
    auto_mode_thread_instance.start()

def unset_auto_mode():
    global auto_mode_thread_instance
    
    if auto_mode_thread_instance is None:
        return
        
    auto_mode_stop_event.set()
    auto_mode_thread_instance.join(timeout=1.0)  # Wait up to 1 second for thread to finish
    auto_mode_thread_instance = None