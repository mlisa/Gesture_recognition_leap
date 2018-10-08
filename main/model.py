import Leap
from enum import Enum

def fingersFromHand(hand):
    thumb = hand.fingers.finger_type(Leap.Finger.TYPE_THUMB)[0]
    index = hand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
    middle = hand.fingers.finger_type(Leap.Finger.TYPE_MIDDLE)[0]
    ring = hand.fingers.finger_type(Leap.Finger.TYPE_RING)[0]
    pinky = hand.fingers.finger_type(Leap.Finger.TYPE_PINKY)[0]

    fingers = dict(thumb=thumb, index=index, middle=middle, ring=ring, pinky=pinky)

    return fingers

class Gesture(Enum):
    gesture0 = (0, "Gesto 0")
    gesture1 = (1, "Gesto 1")
    gesture2 = (2, "Gesto 2")

    def __init__(self, value, name):
        self.code = value
        self.gesture_name = name

    @staticmethod
    def gesture_from_code(code):
        if code == 0:
            return Gesture.gesture0
        elif code == 1:
            return Gesture.gesture1
        elif code == 2:
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

    def __init__(self, hand, previous_palm_position, vector=None):
        self.fingers = []
        if vector is None:
            self.delta_palm_position = Leap.Vector.__sub__(hand.palm_position, previous_palm_position)
            self.arm_angle = hand.direction.angle_to(hand.arm.direction) * Leap.RAD_TO_DEG

            fingers = fingersFromHand(hand)

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
            self.index = FingerModel(Leap.Finger.TYPE_INDEX, vector[6], vector[7], vector[8])
            self.middle = FingerModel(Leap.Finger.TYPE_MIDDLE, vector[9], vector[10], vector[11])
            self.ring = FingerModel(Leap.Finger.TYPE_RING, vector[12], vector[13], vector[14])
            self.pinky = FingerModel(Leap.Finger.TYPE_PINKY, vector[15], vector[16], vector[17])

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

class AvolaModel:
        def __init__(self, hand):
            fingers = fingersFromHand(hand)

            w0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            w1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            w2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            w3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            w4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)

            b0 = fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction.angle_to(fingers['thumb'].bone(Leap.Bone.TYPE_METACARPAL).direction)
            b1 = fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['index'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            b2 = fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['middle'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            b3 = fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['ring'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            b4 = fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['pinky'].bone(Leap.Bone.TYPE_PROXIMAL).direction)

            u0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
            v0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
            z0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

            u1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
            v1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
            z1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

            u2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
            v2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
            z2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

            u3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
            v3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
            z3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

            u4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
            v4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
            z4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

            u5 = hand.palm_position.x
            v5 = hand.palm_position.y
            z5 = hand.palm_position.z

            y1 = fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            y2 = fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            y3 = fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)

            self.feature_list = [w0, w1, w2, w3, w4,
                                b0, b1, b2, b3, b4,
                                u0, v0, z0,
                                u1, v1, z1,
                                u2, v2, z2,
                                u3, v3, z3,
                                u4, v4, z4,
                                u5, v5, z5,
                                y1, y2, y3]

class LuModel:
    def __init__(self, hand, M):
        C = hand.palm_position
        fingers = fingersFromHand(hand)
        features = []
        for finger in fingers:
            features.append(finger.bone(Leap.Bone.TYPE_DISTAL).next_joint.distance_to(C)/M)

        for finger in fingers:
            pass #TODO
            #features.append(finger.bone(Leap.Bone.TYPE_DISTAL).next_joint.

class Sequence:

    def __init__(self):
        self.data_list = []

    def add_data(self, data):
        self.data_list.append(data)

    def discretize(self, value):
        return round(value, 1)

    def raw_data(self):
        raw_data_list = []
        if isinstance(self.data_list[0], HandModel):
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

        elif isinstance(self.data_list[0], AvolaModel):
            for avola_model in self.data_list:
                raw_data_list.append(avola_model.feature_list)

        return raw_data_list



class ClassifiedSequence:

    def __init__(self, sequence, gesture):
        self.sequence = sequence
        self.gesture = gesture

    def to_dict(self):
        return dict(gesture=self.gesture.code, sequence=self.sequence.raw_data())

