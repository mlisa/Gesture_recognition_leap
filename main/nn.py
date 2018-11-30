import tensorflow as tf
import numpy as np
import copy
import matrix as m


class RNN:
    use_model = False

    def __init__(self, params, steps):

        self.n_steps = steps
        self.n_inputs = params['input']
        self.n_neurons = params['neuron']
        self.n_outputs = params['output']
        self.n_layers = params['layer']
        self.learning_rate = params['rate']
        self.n_epochs = params['epoch']
        self.batch_size = params['batch']

        self.input_data = tf.placeholder(tf.float32, [None, self.n_steps, self.n_inputs])
        self.output_data = tf.placeholder(tf.int32, [None])

        lstm_cell = [tf.contrib.rnn.BasicLSTMCell(self.n_neurons) for _ in range(self.n_layers)]
        multi_cell = tf.contrib.rnn.MultiRNNCell(lstm_cell)
        self.outputs, self.final_output = tf.nn.dynamic_rnn(multi_cell, self.input_data, dtype=tf.float32)

        # lstm_cell = tf.contrib.cudnn_rnn.CudnnLSTM(self.n_layers, self.n_neurons)
        # self.outputs, self.final_output = lstm_cell(inputs=self.input_data)

        # gru_cell = [tf.contrib.rnn.GRUBlockCellV2(num_units=self.n_neurons) for _ in range(self.n_layers)]
        # multi_cell = tf.contrib.rnn.MultiRNNCell(gru_cell)
        # self.outputs, self.final_output = tf.nn.dynamic_rnn(multi_cell, self.input_data, dtype=tf.float32)

        top_layer_h_state = self.final_output[-1][1]
        self.logits = tf.layers.dense(top_layer_h_state, self.n_outputs)
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.output_data, logits=self.logits)
        self.loss = tf.reduce_mean(xentropy, name="loss")

        self.loss_writer = tf.summary.FileWriter("../log/loss", tf.get_default_graph())
        self.train_writer = tf.summary.FileWriter("../log/train", tf.get_default_graph())
        self.test_writer = tf.summary.FileWriter("../log/test", tf.get_default_graph())
        optimizer = tf.train.MomentumOptimizer(self.learning_rate, 0.9, use_nesterov=True)
        self.training_op = optimizer.minimize(self.loss)
        correct = tf.nn.in_top_k(self.logits, self.output_data, 1)
        self.accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

        self.loss_summary = tf.summary.scalar("Loss", self.loss)
        self.accuracy_summary = tf.summary.scalar("Accuracy", self.accuracy)

        self.init = tf.global_variables_initializer()
        self.model_saver = tf.train.Saver()

    def train_net(self, training_data, test_data):
        with tf.Session() as sess:
            self.init.run()
            self.accuracy_train = 0.0
            training_input, training_output = self.compute_batch(training_data)
            for epoch in range(self.n_epochs):
                training_list = copy.copy(training_data)
                while len(training_list) > self.batch_size:
                    batch = training_list[:self.batch_size]
                    del training_list[:self.batch_size]
                    self.input_batch, self.output_batch = self.compute_batch(batch)
                    sess.run(self.training_op,
                             feed_dict={self.input_data: self.input_batch, self.output_data: self.output_batch})

                test_input, test_output = self.compute_batch(test_data)
                self.result = []
                for data in test_input:
                    output_val = sess.run(self.logits, feed_dict={self.input_data: [data]})
                    self.result.append(np.argmax(output_val[0]))
                loss_summary = self.loss_summary.eval(feed_dict={self.input_data: training_input, self.output_data: training_output})


                self.loss_writer.add_summary(loss_summary, epoch)
                accuracy = self.accuracy_summary.eval(feed_dict={self.input_data: training_input, self.output_data: training_output})
                self.train_writer.add_summary(accuracy, epoch)
                self.train_writer.flush()
                accuracy = self.accuracy_summary.eval(feed_dict={self.input_data: test_input, self.output_data: test_output})
                self.test_writer.add_summary(accuracy, epoch)
                self.test_writer.flush()

                labels = ["Extrusion", "Scaling enlargement", "Rotation", "Translation", "Right swipe", "Left swipe", "Close", "Scaling reduction"]
                img_d_summary_writer = tf.summary.FileWriter("../log/cf", tf.get_default_graph() )
                img_d_summary = m.ConfusionMatrix.plot_confusion_matrix(test_output, self.result, labels)
                img_d_summary_writer.add_summary(img_d_summary, epoch)

                self.model_saver = tf.train.Saver()
                self.model_saver.save(sess, "/tmp/model-saved.ckpt")

                self.accuracy_train = self.accuracy.eval(feed_dict={self.input_data: training_input,
                                                                    self.output_data: training_output})
                if epoch % 50 == 0 or epoch == self.n_epochs - 1:
                    print "Epoch " + str(epoch) + ": accuracy on training set " + str(self.accuracy_train)

        self.is_trained = True


    def predict(self, x_seq):
        with tf.Session() as sess:
            self.model_saver.restore(sess, "/tmp/model-saved.ckpt")
            output_val = sess.run(self.logits,
                                  feed_dict={self.input_data: x_seq})
        return np.argmax(output_val[0])

    def load_model(self, model_name):
        self.use_model = True
        self.model_to_load = model_name

    def compute_batch(self, data_list):
        input_batch = []
        output_batch = []
        for elem in data_list:
            data = elem.to_dict()
            input_batch.append(data['sequence'])
            output_batch.append(data['gesture'])
        return input_batch, output_batch
