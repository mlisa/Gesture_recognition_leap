import model as m
import file_manager as fl

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

    for i in range(16):
        saver.add_data_to_file(classified_sequence_list[i * 50: i * 50 + 50], "avola_dataset" + str(i))
