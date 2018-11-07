import model as m
import file_manager as fl
import nn as net


class Controller:

    def __init__(self, reader, params):
        self.reader = reader
        self.classified_sequences_list = []
        self.gui = None
        self.classified_data_list = []
        self.sequence_to_classify = []
        self.init_net(params)
        self.setFPS(params['fps'], params['time'])

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

    def read_new_gesture(self):
        self.sequence_to_classify = []
        sequence = self.read_from_leap()

        self.sequence_to_classify = sequence.raw_data()

    def add_to_list(self, classified_sequence):
        self.classified_sequences_list.append(classified_sequence)
        print "Added new sequence to data"

    def save_to_file(self, file_name):
        saver = fl.Saver()
        saver.add_data_to_file(self.classified_sequences_list, file_name)
        self.classified_sequences_list = []
        print "Saved file " + file_name

    def open_training_file(self, file_name):
        self.training_data = self.open_file_data(file_name)

    def open_test_file(self, file_name):
        self.test_data = self.open_file_data(file_name)

    def open_file_data(self, file_name):
        loader = fl.Loader()
        print "Opened file " + file_name
        return loader.load_file(file_name)

    def load_model(self, model_name):
        self.rnn.load_model(model_name)
        print "Loaded " + model_name

    def train(self):
        self.rnn.train_net(self.training_data)

    def test(self):
        confusion_matrix =[[0 for x in range(7)] for y in range(7)]
        correct = 0
        test_size = len(self.test_data)
        for classified_sequence in self.test_data:
            predict_gesture = self.rnn.predict(classified_sequence.sequence)
            confusion_matrix[classified_sequence.gesture][predict_gesture] += 1
            if predict_gesture == classified_sequence.gesture:
                correct += 1

        accuracy = correct * 100 / test_size


    def classify(self):
        gesture = self.rnn.predict([self.sequence_to_classify])
        print "GESTURE" + str(gesture)
        return m.Gesture.gesture_from_code(gesture)
