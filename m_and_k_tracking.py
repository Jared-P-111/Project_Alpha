from pynput import mouse, keyboard
from pprint import pprint
from time import perf_counter, time, sleep
import os
import json
import threading
import pyautogui


class MouseAndKeyTracking:

    #CONSTANTS
    OUTPUT_FILENAME = 'actions_test_01'
    __FILE__ = './data'

    #PROPERTIES
    #Declare mouse_listener globally so we can stop thread with keyboard
    mouse_listener = None
    #Declare start time so callbacks can reference it
    start_time = perf_counter()
    #Store unreleased keyboard key press
    unreleased_keys = []
    #Store all input events
    input_events = []

    class EventType():
        KEYDOWN = 'keyDown'
        KEYUP = 'keyUp'
        CLICK = 'click'
        POS = 'pos'

    def main(self):
        self.countdownTimer()
        trackThread = threading.Thread(target=tracker.mousePosTicker)
        trackThread.start()
        self.runListeners()
        
        print("Recording Duration: {} seconds".format(self.elapsed_time()))
        global input_events
        #pprint(json.dumps(input_events))

        script_dir = os.path.dirname(self.__FILE__)
        filepath = os.path.join(script_dir, 'data', '{}.json'.format(self.OUTPUT_FILENAME))
        with open(filepath, 'w') as outfile:
            json.dump(self.input_events, outfile, indent=4)

    def elapsed_time(self):
        return perf_counter() - self.start_time

    def countdownTimer(self):
        # Countdown timer
        print("Starting", end="", flush=True)
        for i in range(0, 5):
            print(".", end="", flush=True)
            sleep(1)
        print("Go")

    def mousePosTicker(self):
        button = None
        counter = 200

        while True:
            sleep(.3)
            pos = pyautogui.position()
            self.record_event(self.EventType.POS, self.elapsed_time(), button, pos)
            print("Timestamp TIME: {} , POSITION: {}".format(self.elapsed_time(), pos))
            counter -= 1
            if counter == 0:
                break



    def record_event(self, event_type, event_time, button="none", pos=None):
        self.input_events.append({
            'time': event_time,
            'type': event_type,
            'button': str(button),
            'pos': pos
        })

        if event_type == self.EventType.CLICK:
            print('{} on {} pos {} at {}'.format(event_type, button, pos, event_time))

    def on_press(self, key):
        #we only want to record the first keypress event until key has been released. 
        if key in self.unreleased_keys:
            return
        else:
            self.unreleased_keys.append(key)
        try:
            self.record_event(self.EventType.KEYDOWN, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(self.EventType.KEYDOWN, self.elapsed_time(), key)

    def on_release(self, key):
        #mark key as no longer pressed
        print(self.unreleased_keys)
        try:
            self.unreleased_keys.remove(key)
        except ValueError:
            print('{} released at {}'.format(key))

        print('{} released at {}'.format(key, self.elapsed_time()))

        try:
            self.record_event(self.EventType.KEYUP, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(self.EventType.KEYUP, self.elapsed_time(), key)

        if key == keyboard.Key.esc:
            #Stop mouse listener
            self.mouse_listener.stop()
            #Stop Keyboard listener
            raise keyboard.Listener.StopException()

        

    def on_click(self, x, y, button, pressed):
        global unreleased_press
        if not pressed:
            self.record_event(self.EventType.CLICK, self.elapsed_time(), button, (x, y))
            print('Clicked {} at {} time {}'.format(button, (x, y), self.elapsed_time()))


    def runListeners(self):
        #collect mouse input events
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        self.mouse_listener.wait()
        print("LISTENER RUNNING AT {}".format(time()))

        #Collect keyboard inputs until released
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:

                #Start time globally before thread start
                global start_time
                start_time = time()
                listener.join()



tracker = MouseAndKeyTracking()
tracker.main()


