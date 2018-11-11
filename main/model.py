import Leap
from enum import Enum

class Gesture(Enum):
    extrusion = (0, "Extrusion")
    enlargement = (1, "Scale enlargement")
    rotation = (2, "Rotation")
    translation =  (3, "Traslation")
    right_swipe  =  (4, "Right Swipe")
    left_swipe =  (5, "Left Swipe")
    close =  (6, "Close")
    reduction = (7, "Scale reduction")


    def __init__(self, value, name):
        self.code = value
        self.gesture_name = name

    @staticmethod
    def gesture_from_code(code):
        if code == 0:
            return Gesture.extrusion
        elif code == 1:
            return Gesture.enlargement
        elif code == 2:
            return Gesture.rotation
        elif code == 3:
            return Gesture.translation
        elif code == 4:
            return Gesture.right_swipe
        elif code == 5:
            return Gesture.left_swipe
        elif code == 6:
            return Gesture.close
        elif code == 7:
            return Gesture.reduction


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

    def __init__(self, hand, previous_palm_position, vector=None):
        self.fingers = []
        if vector is None:
            self.delta_palm_position = Leap.Vector.__sub__(hand.palm_position, previous_palm_position)
            self.arm_angle = hand.direction.angle_to(hand.arm.direction) * Leap.RAD_TO_DEG

            fingers = self.fingersFromHand(hand)

            for _, finger in fingers.iteritems():
                hand_direction = hand.direction
                proximal_angle = finger.bone(Leap.Bone.TYPE_PROXIMAL).direction.angle_to(
                    hand_direction) * Leap.RAD_TO_DEG
                distal_angle = finger.bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(
                    hand_direction) * Leap.RAD_TO_DEG

                if finger.type != Leap.Finger.TYPE_THUMB:
                    intermediate_angle = finger.bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                        hand_direction) * Leap.RAD_TO_DEG
                    self.add_finger(
                        FingerModel(finger.type, proximal_angle, distal_angle, intermediate_angle))
                else:
                    self.add_finger(
                        FingerModel(finger.type, proximal_angle, distal_angle))
        else:
            self.delta_palm_position = Leap.Vector(vector[0], vector[1], vector[2])
            self.arm_angle = vector[3]
            self.thumb = FingerModel(Leap.Finger.TYPE_THUMB, vector[4], vector[5])
            self.fingers.append(self.thumb)
            self.index = FingerModel(Leap.Finger.TYPE_INDEX, vector[6], vector[7], vector[8])
            self.fingers.append(self.index)
            self.middle = FingerModel(Leap.Finger.TYPE_MIDDLE, vector[9], vector[10], vector[11])
            self.fingers.append(self.middle)
            self.ring = FingerModel(Leap.Finger.TYPE_RING, vector[12], vector[13], vector[14])
            self.fingers.append(self.ring)
            self.pinky = FingerModel(Leap.Finger.TYPE_PINKY, vector[15], vector[16], vector[17])
            self.fingers.append(self.pinky)

    def add_finger(self, finger):
        if finger.type is Leap.Finger.TYPE_THUMB:
            self.thumb = finger
        elif finger.type is Leap.Finger.TYPE_INDEX:
            self.index = finger
        elif finger.type is Leap.Finger.TYPE_MIDDLE:
            self.middle = finger
        elif finger.type is Leap.Finger.TYPE_RING:
            self.ring = finger
        elif finger.type is Leap.Finger.TYPE_PINKY:
            self.pinky = finger
        self.fingers.append(finger)

    def print_hand(self):
        print "Palm position: ", self.delta_palm_position, "\n Arm angle:", self.arm_angle
        for finger in self.fingers:
            finger.print_finger()

    @staticmethod
    def fingersFromHand(hand):
        thumb = hand.fingers.finger_type(Leap.Finger.TYPE_THUMB)[0]
        index = hand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
        middle = hand.fingers.finger_type(Leap.Finger.TYPE_MIDDLE)[0]
        ring = hand.fingers.finger_type(Leap.Finger.TYPE_RING)[0]
        pinky = hand.fingers.finger_type(Leap.Finger.TYPE_PINKY)[0]

        fingers = dict(thumb=thumb, index=index, middle=middle, ring=ring, pinky=pinky)

        return fingers

class DiscretizedHandModel:

    def __init__(self, hand_model):
        self.fingers = []
        for finger in hand_model.fingers:
            discretized_proximal_angle = self.discretize(finger.proximal_angle)
            discretized_distal_angle = self.discretize(finger.distal_angle)
            if finger.type != Leap.Finger.TYPE_THUMB:
                discretized_intermediate_angle = self.discretize(finger.intermediate_angle)
                self.add_finger(FingerModel(finger.type,
                                                                discretized_proximal_angle,
                                                                discretized_distal_angle,
                                                                discretized_intermediate_angle))
            else:
                self.add_finger(FingerModel(finger.type,
                                                                discretized_proximal_angle,
                                                                discretized_distal_angle))
        self.delta_palm_position = hand_model.delta_palm_position
        self.arm_angle = self.discretize(hand_model.arm_angle)

    def add_finger(self, finger):
        if finger.type is Leap.Finger.TYPE_THUMB:
            self.thumb = finger
        elif finger.type is Leap.Finger.TYPE_INDEX:
            self.index = finger
        elif finger.type is Leap.Finger.TYPE_MIDDLE:
            self.middle = finger
        elif finger.type is Leap.Finger.TYPE_RING:
            self.ring = finger
        elif finger.type is Leap.Finger.TYPE_PINKY:
            self.pinky = finger
        self.fingers.append(finger)

    def discretize(self, value):
        return round(value, 1)

    def print_hand(self):
        print "Palm position: ", self.delta_palm_position, "\n Arm angle:", self.arm_angle
        for finger in self.fingers:
            finger.print_finger()


class Sequence:

    def __init__(self):
        self.data_list = []

    def add_data(self, data):
        self.data_list.append(data)

    def load_data(self, list):
        self.data_list = list

    def discretize(self, value):
        return round(value, 1)

    def raw_data(self):
        raw_data_list = []
        if isinstance(self.data_list[0], DiscretizedHandModel):
            for hand_model in self.data_list:
                raw_data = [self.discretize(hand_model.delta_palm_position.x), self.discretize(hand_model.delta_palm_position.y),
                           self.discretize(hand_model.delta_palm_position.z), hand_model.arm_angle]

                raw_data.append(hand_model.thumb.proximal_angle)
                raw_data.append(hand_model.thumb.distal_angle)

                raw_data.append(hand_model.index.proximal_angle)
                raw_data.append(hand_model.index.intermediate_angle)
                raw_data.append(hand_model.index.distal_angle)

                raw_data.append(hand_model.middle.proximal_angle)
                raw_data.append(hand_model.middle.intermediate_angle)
                raw_data.append(hand_model.middle.distal_angle)

                raw_data.append(hand_model.ring.proximal_angle)
                raw_data.append(hand_model.ring.intermediate_angle)
                raw_data.append(hand_model.ring.distal_angle)

                raw_data.append(hand_model.pinky.proximal_angle)
                raw_data.append(hand_model.pinky.intermediate_angle)
                raw_data.append(hand_model.pinky.distal_angle)

                raw_data_list.append(raw_data)
        else:
            return self.data_list

        return raw_data_list


class ClassifiedSequence:

    def __init__(self, sequence, gesture):
        self.sequence = sequence
        self.gesture = gesture

    def to_dict(self):
        return dict(gesture=self.gesture.code, sequence=self.sequence.raw_data())