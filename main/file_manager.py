import json
import pickle as p
import model as m
import struct
import ctypes
import os
import Leap


class Saver:

    def add_data_to_file(self, classified_sequence_list, file_name):
        output = []
        for classified_sequence in classified_sequence_list:
            seq = dict(gesture=classified_sequence.gesture.code, sequence=classified_sequence.sequence.raw_data())
            output.append(seq)
        with open('../data/' + file_name + '.json', 'w') as outfile:
            json.dump(output, outfile)

    def save_raw_data(self, classified_raw_sequence_list, file_name):

        with open("../data/raw/" + file_name + ".data", "wb") as data_file:
            for classified_sequence in classified_raw_sequence_list:
                for frame in classified_sequence.sequence.data_list:
                    serialized_tuple = frame.serialize
                    data = serialized_tuple[0]
                    size = serialized_tuple[1]
                    data_file.write(struct.pack("i", size))

                    data_address = data.cast().__long__()
                    buffer = (ctypes.c_ubyte * size).from_address(data_address)
                    data_file.write(buffer)
                data_file.write(struct.pack("i", classified_sequence.gesture.code))

    def load_raw_data(self, file_name):
        classified_sequence_list = []
        with open("../data/raw/" + file_name + ".data", "rb") as data_file:
            for j in range(0, 16):
                frame_list = []
                for i in range(0, 60):
                    next_block_size = data_file.read(4)
                    size = struct.unpack('i', next_block_size)[0]
                    data = data_file.read(size)
                    leap_byte_array = Leap.byte_array(size)
                    address = leap_byte_array.cast().__long__()
                    ctypes.memmove(address, data, size)

                    frame = Leap.Frame()
                    frame.deserialize((leap_byte_array, size))
                    frame_list.append(frame)
                code = struct.unpack('i', data_file.read(4))[0]
                classified_sequence_list.append(
                    m.ClassifiedSequence(m.Sequence().load_data(frame_list), m.Gesture.gesture_from_code(code)))
        return classified_sequence_list


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
                    sequence.add_data(m.DiscretizedHandModel(m.HandModel(None, None, vector)))

                classified_sequence_list.append(m.ClassifiedSequence(sequence, gesture))

        return classified_sequence_list


if __name__ == '__main__':
    saver = Saver()
    saver.load_raw_data("../data/raw_asd")
