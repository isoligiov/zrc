import subprocess
import pytesseract
import pyautogui
from pynput.mouse import Controller as MouseController
import time
from PIL import Image

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

def get_all_zoom_windows(window_title):
    script = """
activate application "zoom.us"
tell application "System Events"
    set p to first process where it is frontmost
    set result
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

def get_zoom_window_rects():
    script = """
activate application "zoom.us"
tell application "System Events"
	set p to first process where it is frontmost
	set res to ""
	repeat with w in every window of p
		set res to res & (name of w as string) & "\n"
		set window_position to the position of w
		set window_size to the size of w
		set formatted_position to item 1 of window_position & "," & item 2 of window_position
		set formatted_size to item 1 of window_size & "," & item 2 of window_size
		set res to res & (formatted_position as string) & "," & (formatted_size as string) & "\n"
	end repeat
	return res
end tell
"""
    exec_result = execute_apple_script(script)
    lines = exec_result.split('\n')
    result = []
    for i in range(0, len(lines), 2):
        window_name = lines[i]
        rect_str = lines[i + 1]
        bounds = [ int(num) for num in rect_str.split(',') ]
        result.append((window_name, bounds))
    return result

def get_logical_screen_size():
    script = """
tell application "Finder"
	set screen_resolution to bounds of window of desktop
	return screen_resolution
end tell
"""
    rect_str = execute_apple_script(script)
    print(rect_str)
    return [ int(num.strip()) for num in rect_str.split(',') ]

def filter_lowercase_alpha(input_string):
    return ''.join([char for char in input_string if 'a' <= char <= 'z'])

def find_text_position(image, target_text, lang='eng'):
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data['text']):
        if target_text.lower() in filter_lowercase_alpha(word.lower().strip()):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            return x, y, w, h
    return None

def screenshot_region(region=None, save_path=None):
    screenshot = pyautogui.screenshot(region=region)
    if save_path:
        screenshot.save(save_path)
    return screenshot

def min_rgb_filter(img):
    img = img.convert("RGB")
    
    # Get image dimensions
    width, height = img.size

    # Process every pixel
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            minimum_value = min(r, g, b)
            
            # Setting all three channels to the minimum value
            img.putpixel((x, y), (minimum_value, minimum_value, minimum_value))
    return img

def find_admit_button():
    windows = get_zoom_window_rects()
    logical_left, logical_top, logical_right, logical_bottom = get_logical_screen_size()
    physical_width, physical_height = pyautogui.size()
    scalex = physical_width // (logical_right - logical_left)
    scaley = physical_height // (logical_bottom - logical_top)
    for window_index, window in enumerate(windows):
        try:
            window_left, window_top, window_width, window_height = window[1]
            img_save_path = f'screenshot_{window_index}.png'
            zoom_screenshot = screenshot_region(
                (
                    window_left * scalex,
                    window_top * scaley,
                    window_width * scalex,
                    min(window_height, 200) * scaley
                ),
                img_save_path
            )
            filtered_image = min_rgb_filter(zoom_screenshot)
            filtered_image.save(img_save_path)
            admit_position = find_text_position(filtered_image, 'Admit')
            if admit_position is not None:
                # physical_width, physical_height = pyautogui.size()
                x, y, w, h = admit_position
                centerx = window_left + (x + w // 2) / scalex
                centery = window_top + (y + h // 2) / scaley
                return centerx, centery
                # logicalx = centerx / physical_width * (logical_right - logical_left)
                # logicaly = centery / physical_height * (logical_bottom - logical_top)
                # return logicalx, logicaly
                # return region[0] + x + w // 2, region[1] + y + h // 2
        except:
            pass
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