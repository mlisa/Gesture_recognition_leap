import Leap
import model as m
import time


class LeapReader:

    def __init__(self, fps, timeout):
        self.fps = fps
        self.controller = Leap.Controller()
        self.timeout = timeout
        self.data = m.Sequence()
        self.avola_data = m.Sequence()
        self.frames = []
        self.timeout_start = None
        self.previous_palm_position = None
        self.done_reading = False
        self.M = 0

    def setting(self, fps, timeout):
        self.fps = fps
        self.timeout = timeout

    def read(self):
        frame = self.controller.frame()
        if frame.is_valid:
            self.frames.append(frame)

    def compute_frame(self, frame):
        for hand in frame.hands:

            if self.previous_palm_position is None:
                self.previous_palm_position = hand.palm_position

            hand_model = m.HandModel(hand, self.previous_palm_position)
            self.previous_palm_position = hand.palm_position

            avola_model = m.AvolaModel(hand)

            self.data.add_data(hand_model)
            self.avola_data.add_data(avola_model)

            #self.data.add_data(self.discretize_data(hand_model))

    def discretize_data(self, hand_model):
        discretized_hand_model = m.HandModel(hand_model.delta_palm_position, self.discretize(hand_model.arm_angle))

        for finger in hand_model.fingers:
            discretized_proximal_angle = self.discretize(finger.proximal_angle)
            discretized_distal_angle = self.discretize(finger.distal_angle)
            if finger.type != Leap.Finger.TYPE_THUMB:
                discretized_intermediate_angle = self.discretize(finger.intermediate_angle)
                discretized_hand_model.add_finger(m.FingerModel(finger.type,
                                                                discretized_proximal_angle,
                                                                discretized_distal_angle,
                                                                discretized_intermediate_angle))
            else:
                discretized_hand_model.add_finger(m.FingerModel(finger.type,
                                                                discretized_proximal_angle,
                                                                discretized_distal_angle))

        return discretized_hand_model

    def discretize(self, value):
        return round(value, 1)

    def read_data_from_leap(self):
        self.done_reading = False
        self.data = m.Sequence()
        self.frames = []
        while self.frames.__len__() < self.fps * self.timeout:
            self.read()
            time.sleep(1.0/self.fps)

        for frame in self.frames:
            self.compute_frame(frame)
        self.done_reading = True

        return self.data, self.avola_data

    def check_if_one_hand(self):
        hands = self.controller.frame().hands
        if self.M == 0 & len(hands) == 1:
            self.M = hands[0].palm_position.distance_to(hands[0].fingers.finger_type(Leap.Finger.TYPE_MIDDLE)
                                                        .bone(Leap.Bone.TYPE_DISTAL).next_joint)
        return len(hands)





