import Tkinter as tk
import model as m


class Gui:

    def check(self):
        self.set_connected(self.controller.is_leap_connected())
        self.set_hand_label(self.controller.check_hands_read())
        self.window.after(500, self.check)

    def __init__(self, controller):
        self.controller = controller
        self.sequence = []

        self.window = tk.Tk()
        self.window.title("Acquisizione dati")
        self.window.geometry('800x500')

        self.connect_label = tk.Label(self.window, text="")
        self.connect_label.grid(column=0, row=0)

        self.hand_label = tk.Label(self.window)
        self.hand_label.grid(column=4, row=0)

        read_btn = tk.Button(self.window, text="Leggi movimento", command=self.read_data)
        read_btn.grid(column=1, row=2)

        add_btn = tk.Button(self.window, text="Aggiungi campione", command=self.add_data)
        add_btn.grid(column=2, row=2)

        self.file_to_save = tk.StringVar()
        self.save_file_text_area = tk.Entry(self.window, textvariable=self.file_to_save, width=10)
        self.save_file_text_area.grid(column=0, row=4)

        save_btn = tk.Button(self.window, text="Salva file", command=self.save_data)
        save_btn.grid(column=1, row=4)

        self.file_to_open = tk.StringVar()
        self.open_file_text_area = tk.Entry(self.window, textvariable=self.file_to_open, width=10)
        self.open_file_text_area.grid(column=0, row=5)

        open_btn = tk.Button(self.window, text="Apri file", command=self.open_data)
        open_btn.grid(column=1, row=5)
        self.avola_model = tk.IntVar()
        avola_model_check = tk.Checkbutton(self.window, text="Modello Avola", variable=self.avola_model)
        avola_model_check.grid(column=2, row=5)
        train_btn = tk.Button(self.window, text="Addestra", command=self.train)
        train_btn.grid(column=3, row=5)

        self.should_save = 0
        #
        #save_model_btn = tk.Checkbutton(self.window, text="Salva modello", variable=self.should_save)
        #save_model_btn.grid(column=3, row=5)

        self.model_to_open = tk.StringVar()
        self.model_to_open.set("model1")
        #self.open_model_text_area = tk.Entry(self.window, textvariable=self.model_to_open)
        #self.open_model_text_area.grid(column=0, row=6)
        #load_model_btn = tk.Button(self.window, text="Carica modello", command=self.load_model)
        #load_model_btn.grid(column=2, row=6)

        self.result = tk.StringVar()
        self.result_text_area = tk.Entry(self.window, textvariable=self.result, width=10)
        self.result_text_area.grid(column=0, row=7)
        new_gesture_btn = tk.Button(self.window, text="Leggi nuovo gesto", command=self.read_new_gesture)
        new_gesture_btn.grid(column=1, row=7)
        classify_btn = tk.Button(self.window, text="Classifica", command=self.classify)
        classify_btn.grid(column=2, row=7)

        init_label = tk.Label(self.window, text="Modifica Rete")
        init_label.grid(column=0, row=8)

        fps_label = tk.Label(self.window, text="FPS:")
        fps_label.grid(column=0, row=9)
        self.fps = tk.IntVar()
        self.fps.set(20)
        fps_text_area = tk.Entry(self.window, textvariable=self.fps, width=5)
        fps_text_area.grid(column=1, row=9)

        timeout_label = tk.Label(self.window, text="Timeout:")
        timeout_label.grid(column=0, row=10)
        self.timeout = tk.IntVar()
        self.timeout.set(3)
        timeout_text_area = tk.Entry(self.window, textvariable=self.timeout, width=5)
        timeout_text_area.grid(column=1, row=10)

        input_label = tk.Label(self.window, text="Input:")
        input_label.grid(column=0, row=11)
        self.input = tk.IntVar()
        self.input.set(31)
        input_text_area = tk.Entry(self.window, textvariable=self.input, width=5)
        input_text_area.grid(column=1, row=11)

        neuron_label = tk.Label(self.window, text="Neuroni per livello:")
        neuron_label.grid(column=0, row=12)
        self.neuron = tk.IntVar()
        self.neuron.set(200)
        neuron_text_area = tk.Entry(self.window, textvariable=self.neuron, width=5)
        neuron_text_area.grid(column=1, row=12)

        layer_label = tk.Label(self.window, text="Livelli:")
        layer_label.grid(column=0, row=13)
        self.layer = tk.IntVar()
        self.layer.set(4)
        layer_text_area = tk.Entry(self.window, textvariable=self.layer, width=5)
        layer_text_area.grid(column=1, row=13)

        output_label = tk.Label(self.window, text="Output:")
        output_label.grid(column=0, row=14)
        self.output = tk.IntVar()
        self.output.set(3)
        output_text_area = tk.Entry(self.window, textvariable=self.output, width=5)
        output_text_area.grid(column=1, row=14)

        rate_label = tk.Label(self.window, text="Learning rate:")
        rate_label.grid(column=0, row=15)
        self.rate = tk.IntVar()
        self.rate.set(0.0001)
        rate_text_area = tk.Entry(self.window, textvariable=self.rate, width=5)
        rate_text_area.grid(column=1, row=15)

        epoch_label = tk.Label(self.window, text="Epoche:")
        epoch_label.grid(column=0, row=16)
        self.epoch = tk.IntVar()
        self.epoch.set(800)
        epoch_text_area = tk.Entry(self.window, textvariable=self.epoch, width=5)
        epoch_text_area.grid(column=1, row=16)

        batch_label = tk.Label(self.window, text="Batch size:")
        batch_label.grid(column=0, row=17)
        self.batch = tk.IntVar()
        self.batch.set(50)
        batch_text_area = tk.Entry(self.window, textvariable=self.batch, width=5)
        batch_text_area.grid(column=1, row=17)

        modify_reader_btn = tk.Button(self.window, text="Modifica Reader", command=self.modify_reader)
        modify_reader_btn.grid(column=2, row=10)

        modify_net_btn = tk.Button(self.window, text="Modifica rete", command=self.modify_net)
        modify_net_btn.grid(column=2, row=17)

        self.gesture = tk.IntVar()

        rad1 = tk.Radiobutton(self.window, variable=self.gesture, text=m.Gesture.gesture0.gesture_name, value=m.Gesture.gesture0.code)
        rad2 = tk.Radiobutton(self.window, variable=self.gesture, text=m.Gesture.gesture1.gesture_name, value=m.Gesture.gesture1.code)
        rad3 = tk.Radiobutton(self.window, variable=self.gesture, text=m.Gesture.gesture2.gesture_name, value=m.Gesture.gesture2.code)
        rad1.grid(column=1, row=3)
        rad2.grid(column=2, row=3)
        rad3.grid(column=3, row=3)

        self.window.after(500, self.check)

        self.window.mainloop()

    def set_connected(self, connected):
        if connected:
            self.connect_label.configure(text="LeapMotion connesso")
        else:
            self.connect_label.configure(text="LeapMotion disconnesso")

    def set_hand_label(self, n_hands):
        if n_hands == 1:
            self.hand_label.configure(text="OK!")
        else:
            self.hand_label.configure(text="Richiesta una sola mano, lette " + str(n_hands))

    def read_data(self):
        self.sequence, self.avola_sequence = self.controller.read_from_leap()
        print "Read " + str(len(self.sequence.data_list)) + " frames"

    def load_model(self):
        self.controller.load_model(self.model_to_open.get())

    def read_new_gesture(self):
        if self.avola_model.get() == 1:
            self.controller.read_new_gesture(True)
        else:
            self.controller.read_new_gesture(False)

    def add_data(self):
        gesture = m.Gesture.gesture_from_code(self.gesture.get())
        classified_sequence = m.ClassifiedSequence(self.sequence, gesture)
        avola_classified_sequence = m.ClassifiedSequence(self.avola_sequence, gesture)

        self.controller.add_to_list(classified_sequence, avola_classified_sequence)

    def save_data(self):
        self.controller.save_to_file(self.file_to_save.get())

    def open_data(self):
        self.controller.open_file_data(self.file_to_open.get())

    def train(self):
        if self.should_save == 1:
            self.controller.train(True, self.model_to_open.get())
        else:
            self.controller.train(False)

    def classify(self):
        gesture = self.controller.classify()
        self.result.set(gesture.name)

    def modify_reader(self):
        self.controller.setFPS(self.fps.get(), self.timeout.get())

    def modify_net(self):
        params = {}
        params['input'] = self.input.get()
        params['neuron'] = self.neuron.get()
        params['output'] = self.output.get()
        params['layer'] = self.layer.get()
        params['rate'] = self.rate.get()
        params['epoch'] = self.epoch.get()
        params['batch'] = self.batch.get()
        self.controller.init_net(params)
        print "Network initialized"
