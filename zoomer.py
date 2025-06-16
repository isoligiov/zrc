from pyautogui import press, hotkey, click
from utils import (
  bring_zoom_window_to_top,
  zoom_window_exists,
  hide_zoom_window,
  find_text_in_screen,
  move_mouse_smoothly,
)
import time
import os
import subprocess
import sys
from config import ZOOM_APP_WINDOWS_PATH

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
  
  # Wait for Join Audio window
  join_audio_found = 'no'
  for i in range(3):
    join_audio_found = zoom_window_exists("Join audio")
    time.sleep(3)
    if join_audio_found == 'yes':
      break

  # if join audio window is created, confirm join audio
  if join_audio_found == 'yes':
    bring_zoom_window_to_top("Join audio")
    time.sleep(.5)
    print('join audio found')
    for i in range(3):
      press('enter')
      time.sleep(3)
      join_audio_found = zoom_window_exists("Join audio")
      if join_audio_found == 'no':
        break

  for i in range(5):
    press('enter')
    time.sleep(1)
    switch_window()
    time.sleep(1)
  
  # Share screen
  time.sleep(1)
  share_screen()

def approve_remote_control():
  bring_zoom_window_to_top("control")
  time.sleep(1)
  approve_position = find_text_in_screen('Approve', 400)
  if approve_position is None:
    print('Approve button not found')
    return
  x, y = approve_position
  move_mouse_smoothly(x, y, duration=0.5)
  click(x, y)

  time.sleep(0.5)
  confirm_position = find_text_in_screen('Confirm', 300)
  if confirm_position is None:
    print('Confirm button not found')
    return
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