from pyautogui import press, hotkey, click
from utils import (
  bring_zoom_window_to_top,
  zoom_window_exists,
  hide_zoom_window,
  find_admit_button,
)
import time
import os

def open_zoom_app():
  os.system("open /Applications/zoom.us.app")

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
    hotkey('command', 'ctrl', 'v')
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
      print('enter')
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
  time.sleep(.5)
  share_screen()

def approve_remote_control():
  bring_zoom_window_to_top("control")
  time.sleep(1)
  press('enter')

def share_screen():
  bring_zoom_window_to_top("Zoom Meeting")
  time.sleep(1)
  hotkey('command', 'shift', 's')
  time.sleep(1)

def admit_user():
  bring_zoom_window_to_top("Zoom Meeting")
  x, y = find_admit_button()
  click(x, y)

def focus_zoom_meeting():
  bring_zoom_window_to_top("Zoom Meeting")

def press_enter():
  press('enter')

def switch_tab():
  hotkey('command', '`')

def switch_window():
  hotkey('command', 'tab')

def hide_window():
  hide_zoom_window()