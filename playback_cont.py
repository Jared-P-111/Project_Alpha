import pyautogui
import pydirectinput
from time import sleep, time, perf_counter
import os
import json

__file__ = "./data"

def main():
    initializepydirectinput()
    countdownTimer()
    playActions("actions_test_01.json")

def initializepydirectinput():
    # Initialized pydirectinput
    # https://pydirectinput.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pyautogui.FAILSAFE = True

def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 3):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")

def playActions(filename):
    # Read the file
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir, 
        'data', 
        filename
    )
    with open(filepath, 'r') as jsonfile:
        # parse the json
        data = json.load(jsonfile)
        
        for index, action in enumerate(data):
            action_start_time = perf_counter()

            # look for escape input to exit
            if action['button'] == 'Key.esc':
                break

            # perform the action
            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                pydirectinput.keyDown(key)
                print("keyDown on {}".format(key))
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pydirectinput.keyUp(key)
                print("keyUp on {}".format(key))
            elif action['type'] == 'click':
                pydirectinput.click(action['pos'][0], action['pos'][1])
                print("click on {}".format(action['pos']))
            elif action['type'] == 'pos':
                pyautogui.moveTo(action['pos'][0], action['pos'][1])
                print("Mouse moved to X: {}, Y: {}".format(action['pos'][0], action['pos'][1]))

            # then sleep until next action should occur
            try:
                next_action = data[index + 1]
            except IndexError:
                # this was the last action in the list
                break
            elapsed_time = next_action['time'] - action['time']

            # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
            if elapsed_time < 0:
                raise Exception('Unexpected action ordering.')

            # adjust elapsed_time to account for our code taking time to run
            elapsed_time -= (perf_counter() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print('sleeping for {}'.format(elapsed_time))
            sleep(elapsed_time)


# convert pynput button keys into pydirectinput keys
# https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
# https://pydirectinput.readthedocs.io/en/latest/keyboard.html
def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key


if __name__ == "__main__":
    main()