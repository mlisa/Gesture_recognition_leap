import sys
import os
import test_controller as ctrl

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
    params = {}
    params['input'] = 18
    params['neuron'] = 200
    params['output'] = 8
    params['layer'] = 4
    params['rate'] = 0.0001
    params['epoch'] = 3
    params['batch'] = 64

    training_file = sys.argv[1]
    test_file = sys.argv[2]

    controller = ctrl.TestController(params)

    controller.open_training_file(training_file)
    controller.open_test_file(test_file)

    controller.train()

