from pyautogui import press, hotkey
from utils import bring_zoom_window_to_top, zoom_window_exists
import time

def create_zoom_room():
  bring_zoom_window_to_top("Zoom Workplace")
  time.sleep(1)

  join_audio_found = 'no'
  for i in range(3):
    hotkey('command', 'ctrl', 'v')
    time.sleep(3)
    join_audio_found = zoom_window_exists("Join audio")
    if join_audio_found == 'yes':
      break
  
  if join_audio_found == 'no':
    return False
  
  bring_zoom_window_to_top("Join audio")
  time.sleep(.5)
  press('enter')