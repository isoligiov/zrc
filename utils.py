import subprocess
import pytesseract
import pyautogui
from pynput.mouse import Controller as MouseController
import time

mouse = MouseController()

def execute_apple_script(script):
    osa_command = ['osascript', '-e', script]
    return_value = subprocess.check_output(osa_command)
    return_value = return_value.decode('utf-8').strip()
    return return_value

def bring_zoom_window_to_top(window_title):
    script = """
activate application "zoom.us"
tell application "System Events"
    set p to first process where it is frontmost
    repeat with w in every window of p
        if (name of w) contains "{{title}}" then
            tell p
                perform action "AXRaise" of w
            end tell
        end if
    end repeat
end tell
"""
    script = script.replace("{{title}}", window_title)
    return execute_apple_script(script)

def zoom_window_exists(window_title):
    script = """
activate application "zoom.us"
tell application "System Events"
    set p to first process where it is frontmost
    repeat with w in every window of p
        if (name of w) contains "{{title}}" then
            return "yes"
        end if
    end repeat
end tell
return "no"
"""
    script = script.replace("{{title}}", window_title)
    return execute_apple_script(script)

def hide_zoom_window():
    script = """
tell application "System Events"
    set visible of process "zoom.us" to false
end tell
"""
    return execute_apple_script(script)

def get_window_rect(window_title):
    script = """
activate application "zoom.us"
tell application "System Events"
	set p to first process where it is frontmost
	repeat with w in every window of p
		if (name of w) contains "Zoom Meeting" then
			set window_position to the position of w
			set window_size to the size of w
			set formatted_position to item 1 of window_position & "," & item 2 of window_position
			set formatted_size to item 1 of window_size & "," & item 2 of window_size
			set values to (formatted_position as string) & "," & (formatted_size as string)
			return values
		end if
	end repeat
end tell
return "no"
"""
    script = script.replace("{{title}}", window_title)
    rect_str = execute_apple_script(script)
    return [ int(num) for num in rect_str.split(',') ]

def filter_lowercase_alpha(input_string):
    return ''.join([char for char in input_string if 'a' <= char <= 'z'])

def find_text_position(image, target_text, lang='eng'):
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data['text']):
        print(word)
        if target_text.lower() in filter_lowercase_alpha(word.lower().strip()):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            return x, y, w, h
    return None

def screenshot_region(region=None, save_path=None):
    screenshot = pyautogui.screenshot(region=region)
    if save_path:
        screenshot.save(save_path)
    return screenshot

def find_admit_button():
    zoom_screenshot = screenshot_region(None, 'screenshot.png')
    grayscale_image = zoom_screenshot.convert('L')
    admit_position = find_text_position(grayscale_image, 'Admit')
    if admit_position is not None:
        print(admit_position)
        x, y, w, h = admit_position
        return x + w // 2, y + h // 2
        # return region[0] + x + w // 2, region[1] + y + h // 2
    else:
        return None

def move_mouse_smoothly(target_x, target_y, duration=0.5, steps=150):
    start_x, start_y = pyautogui.position()
    delta_x = target_x - start_x
    delta_y = target_y - start_y

    for i in range(steps):
        # Calculate interpolation factor using easeOutQuint
        t = i / steps
        t = 1 - (1 - t)**5
        
        # Calculate next position
        current_x = start_x + (delta_x * t)
        current_y = start_y + (delta_y * t)

        mouse.position = (int(current_x), int(current_y))
        time.sleep(duration / steps)