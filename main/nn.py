import tensorflow as tf
import numpy as np
import copy


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
        top_layer_h_state = self.final_output[-1][1]
        self.logits = tf.layers.dense(top_layer_h_state, self.n_outputs)
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.output_data, logits=self.logits)
        loss = tf.reduce_mean(xentropy, name="loss")
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.training_op = optimizer.minimize(loss)
        correct = tf.nn.in_top_k(self.logits, self.output_data, 1)
        self.accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

        self.init = tf.global_variables_initializer()
        self.model_saver = tf.train.Saver()


    def train_net(self, training_data, should_save, model_name = None):
        with tf.Session() as sess:
            self.init.run()
            for epoch in range(self.n_epochs):
                print "Epoch " + str(epoch) + "..."
                training_list = copy.copy(training_data)
                while len(training_list) > self.batch_size:
                    batch = training_list[:self.batch_size]
                    del training_list[:self.batch_size]
                    input_batch, output_batch = self.compute_batch(batch)
                    sess.run(self.training_op, feed_dict={self.input_data: input_batch, self.output_data: output_batch})
            if should_save:
                self.model_saver = tf.train.Saver()
                self.model_saver.save(sess, "/tmp/" + model_name + ".ckpt")

        self.is_trained = True
        print "Training done!"

    def predict(self, x_seq):
        with tf.Session() as sess:
            if self.use_model:
                self.model_saver.restore(sess, "/tmp/" + self.model_to_load + ".ckpt")
            else:
                init = tf.global_variables_initializer()
                init.run()
            output_val= sess.run(self.logits, feed_dict={self.input_data: x_seq})
            print output_val[0]
            print "--"
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
