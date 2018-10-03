import tensorflow as tf
import numpy as np
import copy


class RNN:

    n_steps = 60
    n_inputs = 18
    n_neurons = 200
    n_outputs = 3
    n_layers = 4
    learning_rate = 0.001
    n_epochs = 800
    batch_size = 2
    is_trained = False

    def __init__(self):
        self.input_data = tf.placeholder(tf.float32, [None, self.n_steps, self.n_inputs])
        self.output_data = tf.placeholder(tf.int32, [None])

        lstm_cell = [tf.contrib.rnn.BasicLSTMCell(self.n_neurons) for _ in range(self.n_layers)]
        multi_cell = tf.contrib.rnn.MultiRNNCell(lstm_cell)

        self.outputs, self.final_output = tf.nn.dynamic_rnn(multi_cell, self.input_data, dtype=tf.float32)
        top_layer_h_state = self.final_output[-1][1]
        logits = tf.layers.dense(top_layer_h_state, self.n_outputs)
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.output_data, logits=logits)
        loss = tf.reduce_mean(xentropy, name="loss")
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.training_op = optimizer.minimize(loss)
        correct = tf.nn.in_top_k(logits, self.output_data, 1)
        self.accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

        self.init = tf.global_variables_initializer()

    def train_net(self, training_data):
        with tf.Session() as sess:
            self.init.run()
            for epoch in range(self.n_epochs):
                training_list = copy.copy(training_data)
                while len(training_list) > self.batch_size:
                    batch = training_list[:self.batch_size]
                    del training_list[:self.batch_size]
                    input_batch, output_batch = self.compute_batch(batch)
                    sess.run(self.training_op, feed_dict={self.input_data: input_batch, self.output_data: output_batch})

        self.is_trained = True
        print "Training done!"

    def predict(self, x_seq):
        if self.is_trained:
            init = tf.global_variables_initializer()
            with tf.Session() as sess:
                init.run()
                output_val = sess.run(self.outputs, feed_dict={self.input_data: x_seq})
                return np.argmax(output_val)
        else:
            return None

    def compute_batch(self, data_list):
        input_batch = []
        output_batch = []
        for elem in data_list:
            data = elem.to_dict()
            input_batch.append(data['sequence'])
            output_batch.append(data['gesture'])

        return input_batch, output_batch

