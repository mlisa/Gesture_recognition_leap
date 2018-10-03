import leap_reader as lr
import gui as gui
import controller as ctrl

if __name__ == '__main__':

    reader = lr.LeapReader(20, 3)
    controller = ctrl.Controller(reader)
    gui = gui.Gui(controller)
