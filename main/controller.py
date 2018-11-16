import model as m
import file_manager as fl
import nn as net
import Tkinter as tk

class Controller:

    def __init__(self, reader, params):
        self.reader = reader
        self.classified_sequences_list = []
        self.classified_raw_sequences_list = []
        self.gui = None
        self.classified_data_list = []
        self.sequence_to_classify = []
        self.init_net(params)
        self.setFPS(params['fps'], params['time'])

    def setFPS(self, fps, time):
        self.reader.setting(fps, time)

    def init_net(self, params):
        self.rnn = net.RNN(params, self.reader.fps * self.reader.timeout)

    def set_gui(self, gui):
        self.gui = gui

    def is_leap_connected(self):
        return self.reader.controller.is_connected

    def check_hands_read(self):
        return self.reader.check_if_one_hand()

    def read_from_leap(self):
        data, raw_data = self.reader.read_data_from_leap()
        self.gui.output_status.insert(tk.END, "Read " + str(len(data.data_list)) + " frames \n")
        return data, raw_data

    # def read_new_gesture(self):
    #     self.sequence_to_classify = []
    #     sequence = self.read_from_leap()
    #
    #     self.sequence_to_classify = sequence.raw_data()

    def add_to_list(self, classified_sequence, classified_raw_sequence):
        self.classified_sequences_list.append(classified_sequence)
        self.classified_raw_sequences_list.append(classified_raw_sequence)
        self.gui.output_status.insert(tk.END, "Added new sequence to data \n")

    def save_to_file(self, file_name):
        saver = fl.Saver()
        saver.add_data_to_file(self.classified_sequences_list, file_name)
        saver.save_raw_data(self.classified_raw_sequences_list, "raw_" + file_name)
        self.classified_sequences_list = []
        self.classified_raw_sequences_list = []
        self.gui.output_status.insert(tk.END,  "Saved file " + file_name + "\n")

    def open_training_file(self, file_name):
        self.training_data = self.open_file_data(file_name)

    def open_test_file(self, file_name):
        self.test_data = self.open_file_data(file_name)

    def open_file_data(self, file_name):
        loader = fl.Loader()
        self.gui.output_network.insert(tk.END,  "Opened file " + file_name + "\n")
        return loader.load_file(file_name)

    def load_model(self, model_name):
        self.rnn.load_model(model_name)
        self.gui.output_network.insert(tk.END,  "Loaded model  " + model_name + "\n")

    def train(self):
        self.rnn.train_net(self.training_data)
        self.gui.output_network.insert(tk.END, "Training done! \n")

    def test(self):
        confusion_matrix =[[0 for x in range(7)] for y in range(7)]
        correct = 0
        test_size = len(self.test_data)

        for classified_sequence in self.test_data:
            predict_gesture = self.rnn.predict([classified_sequence.sequence.raw_data()])
            confusion_matrix[classified_sequence.gesture.code][predict_gesture] += 1
            if predict_gesture == classified_sequence.gesture.code:
                correct += 1

        accuracy = float(correct) * 100.0 / float(test_size)

        self.gui.output_network.insert(tk.END, "Accuracy " + str(accuracy))
