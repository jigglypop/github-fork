from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re
import tensorflow as tf
import numpy as np
import os


def SentimentAnalysis(request_text):
    path_to_train_file = tf.keras.utils.get_file('train.txt', './train.txt')
    path_to_test_file = tf.keras.utils.get_file('train.txt', './test.txt')
    train_text = open(path_to_train_file, 'rb').read().decode(encoding='utf-8')
    test_text = open(path_to_test_file, 'rb').read().decode(encoding='utf-8')

    train_Y = np.array([[int(row.split('\t')[2])]
                        for row in train_text.split('\n')[1:] if row.count('\t') > 0])
    test_Y = np.array([[int(row.split('\t')[2])]
                       for row in test_text.split('\n')[1:] if row.count('\t') > 0])

    def clean_str(string):
        string = re.sub(r"[^가-힣A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", " \( ", string)
        string = re.sub(r"\)", " \) ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = re.sub(r"\'{2,}", "\'", string)
        string = re.sub(r"\'", "", string)

        return string.lower()

    train_text_X = [row.split('\t')[1] for row in train_text.split('\n')[
        1:] if row.count('\t') > 0]
    train_text_X = [clean_str(sentence) for sentence in train_text_X]
    sentences = [sentence.split(' ') for sentence in train_text_X]

    sentences_new = []
    for sentence in sentences:
        sentences_new.append([word[:5] for word in sentence][:25])
    sentences = sentences_new

    # 토큰화
    tokenizer = Tokenizer(num_words=20000)
    tokenizer.fit_on_texts(sentences)
    train_X = tokenizer.texts_to_sequences(sentences)
    train_X = pad_sequences(train_X, padding='post')

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(20000, 300, input_length=25),
        tf.keras.layers.LSTM(units=50),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # 체크포인트
    checkpoint_path = os.getcwd() + "\\SentimentAnalysis\\training_1\\cp.ckpt"
    # checkpoint_path = "./training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # 체크포인트 콜백 만들기
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                     save_weights_only=True,
                                                     verbose=1)
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    model.load_weights(latest)
    # 학습

    history = model.fit(train_X, train_Y, epochs=1, batch_size=30000,
                        validation_split=0.2, callbacks=[cp_callback])

    test_sentence = request_text
    test_sentence = test_sentence.split(' ')
    test_sentences = []
    now_sentence = []
    for word in test_sentence:
        now_sentence.append(word)
        test_sentences.append(now_sentence[:])

    test_X_1 = tokenizer.texts_to_sequences(test_sentences)
    test_X_1 = pad_sequences(test_X_1, padding='post', maxlen=25)
    prediction = model.predict(test_X_1)
    for idx, sentence in enumerate(test_sentences):
        print(sentence)
        print(prediction[idx])
    negative = round(
        (prediction[idx][0] / (prediction[idx][0] + prediction[idx][1])) * 100, 3)
    positive = round(
        (prediction[idx][1] / (prediction[idx][0] + prediction[idx][1])) * 100, 3)
    return negative, positive

