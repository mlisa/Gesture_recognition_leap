import leap_reader as lr
import gui as gui
import controller as ctrl
import Tkinter as tk

if __name__ == '__main__':
    params = {}
    params['input'] = 18
    params['neuron'] = 200
    params['output'] = 7
    params['layer'] = 4
    params['rate'] = 0.0001
    params['epoch'] = 20
    params['batch'] = 12
    params['fps'] = 20
    params['time'] = 3

    root = tk.Tk()

    reader = lr.LeapReader(20, 3)
    controller = ctrl.Controller(reader, params)
    gui = gui.Gui(root)
    gui.set_controller(controller)
    controller.set_gui(gui)
    gui.run()