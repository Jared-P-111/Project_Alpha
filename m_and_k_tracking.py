from pynput import mouse, keyboard
from pprint import pprint
from time import time, sleep, monotonic
import os
import json

OUTPUT_FILENAME = 'actions_test_01'
__FILE__ = './data'

#Declare mouse_listener globally so we can stop thread with keyboard
mouse_listener = None
#Declare start time so callbacks can reference it
start_time = None
#Store unreleased mouse press
unreleased_press = []
#Store unreleased keyboard key press
unreleased_keys = []
#Store all input events
input_events = []

#ENUMS
class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'

def main():
    countdownTimer()
    runListeners()
    
    print("Recording Duration: {} seconds".format(elapsed_time()))
    global input_events
    #pprint(json.dumps(input_events))

    script_dir = os.path.dirname(__FILE__)
    filepath = os.path.join(script_dir, 'data', '{}.json'.format(OUTPUT_FILENAME))
    with open(filepath, 'w') as outfile:
         json.dump(input_events, outfile, indent=4)

def elapsed_time():
    global start_time
    return time() - start_time

def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 5):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")


def record_event(event_type, event_time, button="none", pos=None):
    global input_events
    input_events.append({
        'time': event_time,
        'type': event_type,
        'button': str(button),
        'pos': pos
    })

    if event_type == EventType.CLICK:
        print('{} on {} pos {} at {}'.format(event_type, button, pos, event_time))

def on_press(key):
    #we only want to record the first keypress event until key has been released. 
    global unreleased_keys
    if key in unreleased_keys:
        return
    else:
        unreleased_keys.append(key)
    try:
        record_event(EventType.KEYDOWN, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYDOWN, elapsed_time(), key)

def on_release(key):
    #mark key as no longer pressed
    global unreleased_keys
    print(unreleased_keys)
    try:
        unreleased_keys.remove(key)
    except ValueError:
        print('{} released at {}'.format(key))

    print('{} released at {}'.format(key, elapsed_time()))

    try:
        record_event(EventType.KEYUP, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYUP, elapsed_time(), key)

    if key == keyboard.Key.esc:
        #Stop mouse listener
        global mouse_listener
        mouse_listener.stop()
        #Stop Keyboard listener
        raise keyboard.Listener.StopException()

    

def on_click(x, y, button, pressed):
    global unreleased_press
    if not pressed:
        record_event(EventType.CLICK, elapsed_time(), button, (x, y))
        print('Clicked {} at {} time {}'.format(button, (x, y), elapsed_time()))


def runListeners():
    #collect mouse input events
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    mouse_listener.wait()
    print("LISTENER RUNNING AT {}".format(time()))

    #Collect keyboard inputs until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:

            #Start time globally before thread start
            global start_time
            start_time = time()
            listener.join()

if __name__ == "__main__":
    main()
