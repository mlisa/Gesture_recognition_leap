import model as m
import file_manager as fl
import nn as net


class Controller:

    def __init__(self, reader):
        self.reader = reader
        self.classified_sequences_list = []
        self.gui = None
        self.classified_data_list = []
        self.avola_classified_data_list = []
        self.sequence_to_classify = []

    def setFPS(self, fps, time):
        self.reader.setting(fps, time)

    def init_net(self, params):
        self.rnn = net.RNN(params, self.reader.fps*self.reader.timeout)

    def set_gui(self, gui):
        self.gui = gui

    def is_leap_connected(self):
        return self.reader.controller.is_connected

    def check_hands_read(self):
        return self.reader.check_if_one_hand()

    def read_from_leap(self):
        return self.reader.read_data_from_leap()

    def read_new_gesture(self, isAvolaModel):
        self.sequence_to_classify = []
        if isAvolaModel:
            a, sequence = self.read_from_leap()
        else:
            sequence, a = self.read_from_leap()

        self.sequence_to_classify = sequence.raw_data()

    def add_to_list(self, classified_sequence, avola_classified_sequence):
        self.classified_sequences_list.append(classified_sequence)
        self.avola_classified_data_list.append(avola_classified_sequence)
        print "Added new sequence to data"

    def save_to_file(self, file_name):
        saver = fl.Saver()
        saver.add_data_to_file(self.classified_sequences_list, file_name)
        saver.add_data_to_file(self.avola_classified_data_list, "avola_" + file_name)
        print "Saved file " + file_name

    def open_file_data(self, file_name):
        loader = fl.Loader()
        self.classified_data_list = loader.load_file(file_name)
        print "Opened file " + file_name

    def load_model(self, model_name):
        self.rnn.load_model(model_name)
        print "Loaded " + model_name

    def train(self, should_save, model_name = None):
        self.rnn.train_net(self.classified_data_list, should_save, model_name)

    def classify(self):
        gesture = self.rnn.predict([self.sequence_to_classify])
        print "GESTURE" + str(gesture)
        return m.Gesture.gesture_from_code(gesture)
