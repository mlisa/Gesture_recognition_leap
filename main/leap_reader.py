import Leap
import model as m
import time


class LeapReader:

    def __init__(self, fps, timeout):
        self.fps = fps
        self.controller = Leap.Controller()
        self.timeout = timeout
        self.data = m.Sequence()
        self.raw_data = m.Sequence()
        self.frames = []
        self.timeout_start = None
        self.previous_palm_position = None
        self.done_reading = False

    def setting(self, fps, timeout):
        self.fps = fps
        self.timeout = timeout

    def read(self):
        frame = self.controller.frame()
        if frame.is_valid:
            self.frames.append(frame)

    def compute_frame(self, frame):
        for hand in frame.hands:
            self.raw_data.add_data(frame)
            if self.previous_palm_position is None:
                self.previous_palm_position = hand.palm_position

            hand_model = m.HandModel(hand, self.previous_palm_position)
            self.previous_palm_position = hand.palm_position
            self.data.add_data(m.DiscretizedHandModel(hand_model))

    def read_data_from_leap(self):

        self.done_reading = False
        self.data = m.Sequence()
        self.raw_data = m.Sequence()
        self.frames = []
        while len(self.frames) < self.fps * self.timeout:
            self.read()
            time.sleep(1.0/self.fps)

        for frame in self.frames:
            self.compute_frame(frame)
        self.done_reading = True

        return self.data, self.raw_data

    def check_if_one_hand(self):
        hands = self.controller.frame().hands
        return len(hands)





