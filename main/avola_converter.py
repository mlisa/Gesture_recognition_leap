import model as m
import file_manager as fl
import Leap


class AvolaModel:
    def __init__(self, hand=None, features=None):
        if hand is not None:
            fingers = m.HandModel.fingers_from_hand(hand)

            e2 = fingers['thumb'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(
                fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            d2 = fingers['index'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(
                fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            c2 = fingers['middle'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(
                fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            b2 = fingers['ring'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(
                fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            a2 = fingers['pinky'].bone(Leap.Bone.TYPE_DISTAL).direction.angle_to(
                fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)

            e1 = fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction.angle_to(
                fingers['thumb'].bone(Leap.Bone.TYPE_METACARPAL).direction)
            d1 = fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['index'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            c1 = fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['middle'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            b1 = fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['ring'].bone(Leap.Bone.TYPE_PROXIMAL).direction)
            a1 = fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['pinky'].bone(Leap.Bone.TYPE_PROXIMAL).direction)

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

            de = fingers['thumb'].bone(Leap.Bone.TYPE_PROXIMAL).direction.angle_to(
                fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            cd = fingers['index'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            bc = fingers['middle'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)
            ab = fingers['ring'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction.angle_to(
                fingers['pinky'].bone(Leap.Bone.TYPE_INTERMEDIATE).direction)

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

if __name__ == '__main__':
    file_names = ["a1", "a2", "ab",
                  "b1", "b2", "bc",
                  "c1", "c2", "cd",
                  "d1", "d2", "de",
                  "e1", "e2",
                  "px", "py", "pz",
                  "x0", "x1", "x2", "x3", "x4",
                  "y0", "y1", "y2", "y3", "y4",
                  "z0", "z1", "z2", "z3", "z4"]
    raw_data = {}

    for filename in file_names:
        file = open("../train/" + filename + ".txt", "r")
        raw_data[filename] = []
        for line in file:
            raw_data[filename].append(map(float, line.split()))

    file_y = open("../train/y_train.txt", "r")
    gestures = []
    for line in file_y:
        gestures.append(int(line))

    classified_sequence_list = []

    for i in range(0, 810):
        sequence = m.Sequence()
        for j in range(0, 200):
            model = []
            for filename in file_names:
                model.append(round(raw_data[filename][i][j],3))
            sequence.add_data(model)
            classified_sequence_list.append(m.ClassifiedSequence(sequence, m.Gesture.gesture_from_code(gestures[i])))
    saver = fl.Saver()

    saver.add_data_to_file(classified_sequence_list, "avola_dataset_all")


    for i in range(10):
        saver.add_data_to_file(classified_sequence_list[i * 50: i * 50 + 50], "2_avola_dataset" + str(i))
    print "done!"
