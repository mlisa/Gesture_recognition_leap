import model as m
import file_manager as fl
import nn as net
import Tkinter as tk

class TestController:

    def __init__(self, params):
        self.classified_sequences_list = []
        self.classified_data_list = []
        self.sequence_to_classify = []
        self.init_net(params)

    def init_net(self, params):
        self.rnn = net.RNN(params, 60)

    def open_training_file(self, file_name):
        self.training_data = self.open_file_data(file_name)

    def open_test_file(self, file_name):
        self.test_data = self.open_file_data(file_name)

    def open_file_data(self, file_name):
        loader = fl.Loader()
        return loader.load_file(file_name)

    def train(self):
        self.rnn.train_net(self.training_data)

    def test(self):
        confusion_matrix =[[0 for x in range(8)] for y in range(8)]
        correct = 0
        test_size = len(self.test_data)

        for classified_sequence in self.test_data:
            predict_gesture = self.rnn.predict([classified_sequence.sequence.raw_data()])
            confusion_matrix[classified_sequence.gesture.code][predict_gesture] += 1
            if predict_gesture == classified_sequence.gesture.code:
                correct += 1

        accuracy = float(correct) * 100.0 / float(test_size)

        for i in range(0,8):
            print confusion_matrix[i]

        print "Done with accuracy: " + str(accuracy)
