import pygubu
import model as m

class Gui(pygubu.TkApplication):

    def set_controller(self, controller):
        self.controller = controller

    def _create_ui(self):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('../res/g.ui')

        self.main_frame = builder.get_object('main_frame', self.master)
        self.set_title('Gesture recognition')

        self.connect_label = builder.get_object("connect_label")
        self.hand_label = builder.get_object("hand_label")

        self.file_to_save = builder.get_variable("file_to_save")
        self.file_to_open = builder.get_variable("file_to_open")

        self.gesture = builder.get_variable("gesture")
        self.total_gestures = builder.get_variable("total_gestures")

        builder.connect_callbacks(self)

        callbacks = {
            'read_data': self.read_data,
            'save_data': self.save_data,
            'add_data': self.add_data,
            'open_data': self.open_data,
            'train': self.train,
            'test': self.test
        }

        builder.connect_callbacks(callbacks)
        self.master.after(500, self.check)


    def check(self):
        self.set_connected(self.controller.is_leap_connected())
        self.set_hand_label(self.controller.check_hands_read())
        self.master.after(500, self.check)


    def read_data(self):
        self.sequence = self.controller.read_from_leap()
        print "Read " + str(len(self.sequence.data_list)) + " frames"

    def set_hand_label(self, n_hands):
        if n_hands == 1:
            self.hand_label.configure(text="OK!")
        else:
            self.hand_label.configure(text="Richiesta una mano, lette " + str(n_hands))


    def set_connected(self, connected):
        if connected:
            self.connect_label.configure(text="LeapMotion connesso")
        else:
            self.connect_label.configure(text="LeapMotion disconnesso")

    def save_data(self):
        self.controller.save_to_file(self.file_to_save.get())
        self.total_gestures.set(str(len(self.controller.classified_sequences_list)))

    def open_data(self):
        self.controller.open_file_data(self.file_to_open.get())

    def add_data(self):
        gesture = m.Gesture.gesture_from_code(self.gesture.get())
        classified_sequence = m.ClassifiedSequence(self.sequence, gesture)

        self.controller.add_to_list(classified_sequence)
        self.total_gestures.set(str(len(self.controller.classified_sequences_list)))

    def train(self):
            self.controller.train()

    def test(self):
        pass