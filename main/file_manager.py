import json
import model as m
import struct
import ctypes
import Leap
import random


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
            print str(len(classified_raw_sequence_list))
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

    def compute_batch(self, data_list):
        input_batch = []
        output_batch = []
        for elem in data_list:
            data = elem.to_dict()
            input_batch.append(data['sequence'])
            output_batch.append(data['gesture'])
        return input_batch, output_batch

class Merger:

    def merge_files(self, file_name_list):
        merged_file_list = []
        loader = Loader()
        for file_name in file_name_list:
            classified_list = loader.load_file(file_name)
            for gesture in classified_list:
                merged_file_list.append(gesture)

        print str(len(merged_file_list))
        random.shuffle(merged_file_list)
        return merged_file_list


if __name__ == '__main__':
    list_1 = ["1_lisa", "2_sara", "3_ramo", "4_ale", "5_gian", "6_must", "7_ilar", "8_chia", "9_mart",
            "10_fabi", "11_vitt", "12_fili", "13_bis", "14_fran", "15_jean", "16_alfr", "17_ele",
            "18_clau", "19_mart", "20_lore", "21_qi", "22_bea", "23_eleo", "24_chia"]
    list_2 = ["25_marc", "26_edo", "31_simo", "28_rob", "29_cla", "30_dav"]
    merger = Merger()
    saver = Saver()
    merged_list = merger.merge_files(list_2)
    saver.add_data_to_file(merged_list, "test")

