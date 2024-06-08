import tensorflow as tf
class CodeSwitchingModel(tf.Module):
    def __init__(self, vocab_size, num_classes, embedding_dim=64, lstm_units=64):
        super(CodeSwitchingModel, self).__init__()
        self.embedding = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)
        self.bilstm = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units, return_sequences=True))
        self.dense = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(num_classes, activation='softmax'))
    
    @tf.function
    def __call__(self, inputs):
        x = self.embedding(inputs)
        x = self.bilstm(x)
        return self.dense(x)
    
    def train_step(self, x, y, loss_fn, optimizer):
        with tf.GradientTape() as tape:
            predictions = self(x)
            loss = loss_fn(y, predictions)
        gradients = tape.gradient(loss, self.trainable_variables)
        optimizer.apply_gradients(zip(gradients, self.trainable_variables))
        return loss
