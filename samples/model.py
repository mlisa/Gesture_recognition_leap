import Leap
from enum import Enum


class Gesture(Enum):
    gesture0 = (0, "Gesto 0")
    gesture1 = (1, "Gesto 1")
    gesture2 = (2, "Gesto 2")

    def __init__(self, value, name):
        self.code = value
        self.name = name

    @staticmethod
    def gesture_from_code(code):
        if code == 0:
            return Gesture.gesture0
        elif code == 1:
            return Gesture.gesture1
        else:
            return Gesture.gesture2


class FingerModel:
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

    def __init__(self, finger_type, proximal, distal, intermediate=None):
        self.type = finger_type
        self.proximal_angle = proximal
        self.intermediate_angle = intermediate
        self.distal_angle = distal

    def print_finger(self):
        print "Finger type", self.finger_names[self.type], "--------- " \
            "\n Proximal angle: ", self.proximal_angle, \
            "\n Intermediate angle:", self.intermediate_angle, \
            "\n Distal angle:", self.distal_angle


class HandModel:

    def __init__(self, delta_palm_position, arm_angle):
        self.fingers = []
        self.delta_palm_position = delta_palm_position
        self.arm_angle = arm_angle

    def discretize(self, value):
        return round(value, 1)

    def add_finger(self, finger):
        self.fingers.append(finger)

    def print_hand(self):
        print "Palm position: ", self.delta_palm_position, "\n Arm angle:", self.arm_angle
        for finger in self.fingers:
            finger.print_finger()

    def raw_data(self):
        raw_data = [self.discretize(self.delta_palm_position.x), self.discretize(self.delta_palm_position.y),
                    self.discretize(self.delta_palm_position.z), self.arm_angle]

        for finger in self.fingers:
            raw_data.append(finger.proximal_angle)
            raw_data.append(finger.distal_angle)
            if finger.type != Leap.Finger.TYPE_THUMB:
                raw_data.append(finger.proximal_angle)

        return raw_data


class Sequence:

    def __init__(self):
        self.data_list = []

    def add_data(self, data):
        self.data_list.append(data)


class ClassifiedSequence:

    def __init__(self, sequence, gesture):
        self.sequence = sequence
        self.gesture = gesture

    def to_dict(self):
        dictionary = dict(gesture=self.gesture.code, sequence=[])
        for data in self.sequence.dataList:
            if type(data) is HandModel:
                dictionary['sequence'].append(data.raw_data())
            else:
                dictionary['sequence'].append(data)

        return dictionary
