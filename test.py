from utils import get_logical_screen_size
import pyautogui

logical_left, logical_top, logical_right, logical_bottom = get_logical_screen_size()
physical_width, physical_height = pyautogui.size()
print(physical_width, physical_height)