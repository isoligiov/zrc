import subprocess
import pytesseract
import pyautogui

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

def find_text_position(image, target_text, lang='eng'):
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data['text']):
        print(word)
        if word.lower() == target_text.lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            return x, y, w, h
    return None

def screenshot_region(region, save_path=None):
    screenshot = pyautogui.screenshot(region=region)
    if save_path:
        screenshot.save(save_path)
    return screenshot

def find_admit_button():
    left, top, width, height = get_window_rect('Zoom Meeting')
    region = (left, top + 50, width, 200)
    zoom_screenshot = screenshot_region(region, 'screenshot.png')
    grayscale_image = zoom_screenshot.convert('L')
    admit_position = find_text_position(grayscale_image, 'Admit')
    if admit_position is not None:
        x, y, w, h = admit_position
        return region[0] + x + w // 2, region[1] + y + h // 2
    else:
        return None
