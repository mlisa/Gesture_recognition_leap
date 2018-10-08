import json
import model as m


class Saver:

    def add_data_to_file(self, classified_sequence_list, file_name):
        output = []
        for classified_sequence in classified_sequence_list:
            seq = dict(gesture=classified_sequence.gesture.code, sequence=classified_sequence.sequence.raw_data())
            output.append(seq)
        print output
        with open('../data/' + file_name + '.json', 'w') as outfile:
            json.dump(output, outfile)

class Loader:

    def load_file(self, file_name):
        classified_sequence_list = []
        with open('../data/' + file_name + '.json') as f:
            data = json.load(f)
            for classified_sequence in data:
                gesture_code = classified_sequence['gesture']
                seq = classified_sequence['sequence']
                sequence = m.Sequence()

                gesture = m.Gesture.gesture_from_code(gesture_code)

                for vector in seq:
                    sequence.add_data(m.HandModel(None, None, vector))

                classified_sequence_list.append(m.ClassifiedSequence(sequence, gesture))

            return classified_sequence_list
