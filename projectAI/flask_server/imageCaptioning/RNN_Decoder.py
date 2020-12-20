import tensorflow as tf
from .BahdanauAttention import BahdanauAttention


class RNN_Decoder(tf.keras.Model):
    def __init__(self, embedding_dim, units, vocab_size):
        super(RNN_Decoder, self).__init__()
        self.units = units
        # 임베딩 embedding_dim = 256차원으로 임베딩 시킨다.
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        # 순환신경망에 GRU를 배치. 현재 RNN과 LSTM을 비롯한 순환신경망이며 성능으로 각광받고 있음
        self.gru = tf.keras.layers.GRU(
            self.units, return_sequences=True, return_state=True, recurrent_initializer='glorot_uniform')
        self.fc1 = tf.keras.layers.Dense(self.units)
        self.fc2 = tf.keras.layers.Dense(vocab_size)
        # 어텐션 계층.
        self.attention = BahdanauAttention(self.units)

    def call(self, x, features, hidden):
        # 어텐션 함수의 결과를 weight와 벡터로 각각 저장
        context_vector, attention_weights = self.attention(features, hidden)
        # 임베딩 레이어를 통과한 후의 x shape -> (batch_size, 1, embedding_dim)
        x = self.embedding(x)
        # embedding과 hidden_size를 결합한 후의 x shape -> (batch_size, 1, embedding_dim + hidden_size)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        # 결합된 벡터를 GRU로 전달
        output, state = self.gru(x)
        # Dense1
        # x shape -> (batch_size, max_length, hidden_size)
        x = self.fc1(output)
        # x shape -> (batch_size * max_length, hidden_size)
        x = tf.reshape(x, (-1, x.shape[2]))
        # Dense2
        # output shape -> (batch_size * max_length, vocab)
        x = self.fc2(x)
        return x, state, attention_weights

    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))
