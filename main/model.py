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
    gesture3 =  (3, "Gesto 3")
    gesture4  =  (4, "Gesto 4")
    gesture5 =  (5, "Gesto 5")
    gesture6 =  (6, "Gesto 6")
    gesture7 =  (7, "Gesto 7")
    gesture8 =  (8, "Gesto 8")
    gesture9 =  (9, "Gesto 9")
    gesture10=  (10, "Gesto 10")
    gesture11 = (11, "Gesto 11")
    gesture12 = (12, "Gesto 12")
    gesture13 = (13, "Gesto 13")
    gesture14 = (14, "Gesto 14")
    gesture15 = (15, "Gesto 15")
    gesture16 = (16, "Gesto 16")
    gesture17 = (17, "Gesto 17")
    gesture18 = (18, "Gesto 18")
    gesture19 = (19, "Gesto 19")
    gesture20 = (20, "Gesto 20")
    gesture21 = (21, "Gesto 21")
    gesture22 = (22, "Gesto 22")
    gesture23 = (23, "Gesto 23")
    gesture24 = (24, "Gesto 24")
    gesture25 = (25, "Gesto 25")
    gesture26 = (26, "Gesto 26")
    gesture27 = (27, "Gesto 27")
    gesture28 = (28, "Gesto 28")
    gesture29 = (29, "Gesto 29")
    gesture30 = (30, "Gesto 30")

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
        elif code == 3:
            return Gesture.gesture3
        elif code == 4:
            return Gesture.gesture4
        elif code == 5:
            return Gesture.gesture5
        elif code == 6:
            return Gesture.gesture6
        elif code == 7:
            return Gesture.gesture7
        elif code == 8:
            return Gesture.gesture8
        elif code == 9:
            return Gesture.gesture9
        elif code == 10:
            return Gesture.gesture10
        elif code == 11:
            return Gesture.gesture11
        elif code == 12:
            return Gesture.gesture12
        elif code == 13:
            return Gesture.gesture13
        elif code == 14:
            return Gesture.gesture14
        elif code == 15:
            return Gesture.gesture15
        elif code == 16:
            return Gesture.gesture16
        elif code == 17:
            return Gesture.gesture17
        elif code == 18:
            return Gesture.gesture18
        elif code == 19:
            return Gesture.gesture19
        elif code == 20:
            return Gesture.gesture20
        elif code == 21:
            return Gesture.gesture21
        elif code == 22:
            return Gesture.gesture22
        elif code == 23:
            return Gesture.gesture23
        elif code == 24:
            return Gesture.gesture24
        elif code == 25:
            return Gesture.gesture25
        elif code == 26:
            return Gesture.gesture26
        elif code == 27:
            return Gesture.gesture27
        elif code == 28:
            return Gesture.gesture28
        elif code == 29:
            return Gesture.gesture29
        elif code == 30:
            return Gesture.gesture30


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
        def __init__(self, hand = None, features = None):
            if hand is not None:
                fingers = fingersFromHand(hand)

                e2 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
                d2 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
                c2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
                b2 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
                a2 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)

                e1 = fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction.angle_to(fingers['thumb'].bone(Leap.Bone.TYPE_METACARPAL).direction)
                d1 = fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['index'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
                c1 = fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['middle'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
                b1 = fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['ring'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
                a1 = fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['pinky'].bone(Leap.Bone.TYPE_PROXIMAL).direction)

                x0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
                y0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
                z0 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

                x1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
                y1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
                z1 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

                x2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
                y2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
                z2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

                x3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
                y3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
                z3 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

                x4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).next_joint.x
                y4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).next_joint.y
                z4 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).next_joint.z

                px = hand.palm_position.x
                py = hand.palm_position.y
                pz = hand.palm_position.z

                de = fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction.angle_to(fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
                cd = fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
                bc = fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
                ab = fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)

                self.feature_list = [a1, a2, ab,
                                     b1, b2, bc,
                                     c1, c2, cd,
                                     d1, d2, de,
                                     e1, e2,
                                     px, py, pz,
                                     x0, x1, x2, x3, x4,
                                     y0, y1, y2, y3, y4,
                                     z0, z1, z2, z3, z4]

            elif features is not None:
                self.feature_list = features

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
        else:
            return self.data_list

        return raw_data_list



class ClassifiedSequence:

    def __init__(self, sequence, gesture):
        self.sequence = sequence
        self.gesture = gesture

    def to_dict(self):
        return dict(gesture=self.gesture.code, sequence=self.sequence.raw_data())

