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
        self.window.geometry('800x250')

        self.connect_label = tk.Label(self.window, text="")
        self.connect_label.grid(column=0, row=0)

        self.hand_label = tk.Label(self.window)
        self.hand_label.grid(column=4, row=0)

        read_btn = tk.Button(self.window, text="Leggi movimento", command=self.read_data)
        read_btn.grid(column=1, row=2)

        add_btn = tk.Button(self.window, text="Aggiungi campione", command=self.add_data)
        add_btn.grid(column=2, row=2)

        self.file_to_save = tk.StringVar()
        self.save_file_text_area = tk.Entry(self.window, textvariable=self.file_to_save)
        self.save_file_text_area.grid(column=0, row=4)

        save_btn = tk.Button(self.window, text="Salva file", command=self.save_data)
        save_btn.grid(column=1, row=4)

        self.file_to_open = tk.StringVar()
        self.file_to_open.set("prova1")
        self.open_file_text_area = tk.Entry(self.window, textvariable=self.file_to_open)
        self.open_file_text_area.grid(column=0, row=5)

        open_btn = tk.Button(self.window, text="Apri file", command=self.open_data)
        open_btn.grid(column=1, row=5)
        train_btn = tk.Button(self.window, text="Addestra", command=self.train)
        train_btn.grid(column=2, row=5)

        self.result = tk.StringVar()
        self.result_text_area = tk.Entry(self.window, textvariable=self.result)
        self.result_text_area.grid(column=0, row=6)
        train_btn = tk.Button(self.window, text="Classifica", command=self.classify)
        train_btn.grid(column=1, row=6)

        self.gesture = tk.IntVar()

        self.rad1 = tk.Radiobutton(self.window, variable=self.gesture, text=m.Gesture.gesture0.name, value=m.Gesture.gesture0.code)
        self.rad2 = tk.Radiobutton(self.window, variable=self.gesture, text=m.Gesture.gesture1.name, value=m.Gesture.gesture1.code)
        self.rad3 = tk.Radiobutton(self.window, variable=self.gesture, text=m.Gesture.gesture2.name, value=m.Gesture.gesture2.code)
        self.rad1.grid(column=1, row=3)
        self.rad2.grid(column=2, row=3)
        self.rad3.grid(column=3, row=3)

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
        self.sequence = self.controller.read_from_leap()

    def add_data(self):
        gesture = m.Gesture.gesture_from_code(self.gesture.get())
        classified_sequence = m.ClassifiedSequence(self.sequence, gesture)

        self.controller.add_to_list(classified_sequence)

    def save_data(self):
        self.controller.save_to_file(self.file_to_save.get())

    def open_data(self):
        self.controller.open_file_data(self.file_to_open.get())

    def train(self):
        self.controller.train()

    def classify(self):
        gesture = self.controller.classify()
        self.result.set(gesture.name)
