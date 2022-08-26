# example of stopping a custom thread class
from time import sleep
from threading import Thread
from threading import Event
from pynput import keyboard

# custom thread class
class CustomThread(Thread):
    # constructor
    def __init__(self, event):
        # call the parent constructor
        super(CustomThread, self).__init__()
        # store the event
        self.event = event
 
    # execute task
    def run(self):
        # execute a task in a loop
        while True:
            # block for a moment
            sleep(1)
            # check for stop
            if self.event.is_set():
                break
        print('Worker closing down')
 
# create the event
event = Event()
# create a new thread
thread = CustomThread(event)
# start the new thread
thread.start()

# callback function for event
def on_release(key):
    if key == keyboard.Key.esc:
        # stop the worker thread
        print('Main stopping thread')
        return event.set()

# create keyboard Listener & Controller
listener = keyboard.Listener(on_release=on_release)
listener.start()

print("All threads are running")

# wait for the new thread to finish
thread.join()

