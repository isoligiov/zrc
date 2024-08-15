import subprocess
import time

for i in range(1000):
    script = """
    activate application "zoom.us"
    tell application "System Events"
        set |res| to ""
        set p to first process where it is frontmost
        repeat with w in every window of p
            set |res| to |res| & "\n" & (name of w)
        end repeat
        return |res|
    end tell
    """
    osa_command = ['osascript', '-e', script]
    return_value = subprocess.check_output(osa_command)
    return_value = return_value.decode('utf-8').strip()
    print(return_value)
    print("==========================")

    time.sleep(5)
