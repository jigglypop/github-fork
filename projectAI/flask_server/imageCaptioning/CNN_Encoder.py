import tensorflow as tf


class CNN_Encoder(tf.keras.Model):
    # pickle을 이용해서 피쳐를 추출해서 완전연결층으로 전달한다 .
    def __init__(self, embedding_dim):
        super(CNN_Encoder, self).__init__()
        # shape after fc == (batch_size, 64, embedding_dim)
        self.fc = tf.keras.layers.Dense(embedding_dim)

    def call(self, x):
        # Dense
        x = self.fc(x)
        # shape after fc == (batch_size, 64, embedding_dim)
        x = tf.nn.relu(x)
        return x
