import os
import time


def square(trtl, length):
    for _ in range(4):
        trtl.forward(length)
        trtl.left(90)


def jump(trtl, x, y):
    trtl.penup()
    trtl.goto(x, y)
    trtl.pendown()


def intersection(listA, listB):
    output = []
    for item in listA:
        if item in listB:
            output.append(item)
    return output


def listAllFilesIn(myPath, extension):
    '''
    Returns a lists all of files in a given path with a given extension

    Dependencies: os
    '''
    filePaths = []
    for (dirpath, _, filenames) in os.walk(myPath):
        for filename in filenames:
            if filename.split('.')[-1] == extension:
                filePath = os.path.join(dirpath, filename)
                filePath = filePath.replace("\\", "/")  # only for windows
                filePaths.append(filePath)

    return filePaths


class EventManager():
    '''
    An event manger for the turtle module that 
    handles multiple keyboard events at the same time

    Dependencies: time
    '''

    def __init__(self):
        self.queue = set()
        self.delay = 0.0
        self.last_time = time.time()

    def bind(self, screen, events):
        '''events = {keyboard_event: event_handler, ...}'''
        screen.listen()
        for k, h in events.items():
            screen.onkeypress(lambda h=h: self.queue.add(h), k)
            screen.onkeyrelease(lambda h=h: self.queue.remove(h), k)

    def handle(self):
        if time.time() - self.last_time > self.delay:
            self.last_time = time.time()
            for handler in self.queue:
                handler()
