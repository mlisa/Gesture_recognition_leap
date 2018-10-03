import model as m
import file_manager as fl
import nn as net


class Controller:

    def __init__(self, reader):
        self.reader = reader
        self.classified_sequences_list = []
        self.rnn = net.RNN()
        self.gui = None
        self.classified_data_list = []

    def set_gui(self, gui):
        self.gui = gui

    def is_leap_connected(self):
        return self.reader.controller.is_connected

    def check_hands_read(self):
        return self.reader.check_if_one_hand()

    def read_from_leap(self):
        return self.reader.read_data_from_leap()

    def add_to_list(self, classified_sequence):
        self.classified_sequences_list.append(classified_sequence)

    def save_to_file(self, file_name):
        saver = fl.Saver()
        saver.add_data_to_file(self.classified_sequences_list, file_name)

    def open_file_data(self, file_name):
        loader = fl.Loader()
        self.classified_data_list = loader.load_file(file_name)

    def train(self):
        self.rnn.train_net(self.classified_data_list)

    def classify(self):
        return m.Gesture.gesture_from_code(self.rnn.predict([]))
