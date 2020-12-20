from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow.python.client import device_lib
import tensorflow as tf

# 맷플롯립
import pprint
import pickle
from PIL import Image
from glob import glob
import json
import time
import os
import numpy as np
import re


# 맷플롯립
import matplotlib.pyplot as plt
# 사이킷런(데이터 분할, 셔플용)

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import cv2

# 모듈 임포트
from .load_image import load_image
from .BahdanauAttention import BahdanauAttention
from .CNN_Encoder import CNN_Encoder
from .RNN_Decoder import RNN_Decoder


def ImageCaption(HttpImagePath):
    # json 파일 읽기
    UPLOAD_DIR = os.getcwd()

    annotation_file = UPLOAD_DIR + \
        '\\imageCaptioning\\annotations\\captions_train2014.json'
    PATH = UPLOAD_DIR + '\\imageCaptioning\\train2014\\'
    with open(annotation_file, 'r') as f:
        annotations = json.load(f)

    # 캡션, 이미지 벡터 저장
    all_captions = []
    all_img_path = []

    for annot in annotations['annotations']:
        # <start>와 <end>를 처음과 끝에 넣어 구분해준다.
        caption = '<start> ' + annot['caption'] + ' <end>'
        image_id = annot['image_id']
        full_coco_image_path = PATH + \
            'COCO_train2014_' + '%012d.jpg' % (image_id)
        # 이미지 패스 저장
        all_img_path.append(full_coco_image_path)
        # 이미지 캡션 저장
        all_captions.append(caption)

    # 캡션과 이미지 섞기
    train_captions, img_path = shuffle(
        all_captions, all_img_path, random_state=1)
    # 섞은 이미지에서 30000개 추출
    num_examples = 30000
    train_captions = train_captions[:num_examples]
    img_path = img_path[:num_examples]

    # 모델 만들기
    image_model = tf.keras.applications.InceptionV3(
        include_top=False, weights='imagenet')
    new_input = image_model.input
    # 마지막 레이어 갈아끼워주는 과정
    hidden_layer = image_model.layers[-1].output
    image_features_extract_model = tf.keras.Model(new_input, hidden_layer)

    # 데이터셋 최고 길이

    def calc_max_length(tensor):
        return max(len(t) for t in tensor)

    # 5000개의 단어만 선택
    top_k = 5000
    tokenizer = tf.keras.preprocessing.text.Tokenizer(
        num_words=top_k, oov_token="<unk>", filters='!"#$%&()*+.,-/:;=?@[\]^_`{|}~ ')
    tokenizer.fit_on_texts(train_captions)
    train_seqs = tokenizer.texts_to_sequences(train_captions)
    tokenizer.word_index['<pad>'] = 0
    tokenizer.index_word[0] = '<pad>'
    # 토큰 벡터 만들기
    train_seqs = tokenizer.texts_to_sequences(train_captions)
    # 각각의 최고 길이에 맞게 길이를 맞추어 준다. 최고길이 값을 파라미터에 정해주지 않으면 자동으로 계산한다.
    # 다음 예제에서는 49가 max값이므로 ex)[1,2,3] -> [1,2,3,0,0,0,0,0,0,0,0,0,...0](49)
    cap_vector = tf.keras.preprocessing.sequence.pad_sequences(
        train_seqs, padding='post')
    # attention weights에 쓰일 최고 길이 계산
    # 49개가 최고값이고 따라서 cap_vector 각각의 길이는 49개가 된다
    max_length = calc_max_length(train_seqs)

    # 데이터셋 분리

    # 데이터셋 8:2로 분리
    img_path_train, img_path_val, cap_train, cap_val = train_test_split(
        img_path, cap_vector, test_size=0.2, random_state=0)

    # 구성용 파라미터 모델 체우기
    BATCH_SIZE = 64
    BUFFER_SIZE = 1000
    embedding_dim = 256
    units = 512
    vocab_size = top_k + 1
    # 스텝은 총 길이 // 배치사이즈
    num_steps = len(img_path_train) // BATCH_SIZE

    # InceptionV3에서 추출할 벡터는 (64,2048)
    features_shape = 2048
    attention_features_shape = 64

    # 넘파이 파일 로딩함수

    def map_func(img_name, cap):
        img_tensor = np.load(img_name.decode('utf-8')+'.npy')
        return img_tensor, cap

    dataset = tf.data.Dataset.from_tensor_slices((img_path_train, cap_train))

    # map 함수를 이용하여 numpy 파일을 평행하게 묶는다.
    dataset = dataset.map(lambda item1, item2: tf.numpy_function(
        map_func, [item1, item2], [tf.float32, tf.int32]),
        num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # 데이터셋 섞기
    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    # 속도 개선을 위하여 프리패칭 진행
    # (GPU의 계산 속도보다 데이터 로딩 속도가 느리기 때문에 미리 유추해서 다음 순서에 가져다 놓는 방식으로 진행하게 된다.)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    # 예제 BATCH_SIZE = 64, embedding_dim = 256, units = 512

    encoder = CNN_Encoder(embedding_dim)
    decoder = RNN_Decoder(embedding_dim, units, vocab_size)

    optimizer = tf.keras.optimizers.Adam()
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction='none')

    def loss_function(real, pred):
        mask = tf.math.logical_not(tf.math.equal(real, 0))
        loss_ = loss_object(real, pred)
        mask = tf.cast(mask, dtype=loss_.dtype)
        loss_ *= mask
        return tf.reduce_mean(loss_)

    checkpoint_path = UPLOAD_DIR + "\\imageCaptioning\\checkpoints\\train"
    ckpt = tf.train.Checkpoint(encoder=encoder,
                               decoder=decoder,
                               optimizer=optimizer)
    ckpt_manager = tf.train.CheckpointManager(
        ckpt, checkpoint_path, max_to_keep=5)

    start_epoch = 0
    if ckpt_manager.latest_checkpoint:
        start_epoch = int(ckpt_manager.latest_checkpoint.split('-')[-1])
        # restoring the latest checkpoint in checkpoint_path
        ckpt.restore(ckpt_manager.latest_checkpoint)

    # 별도 셀에 이것을 추가하는 이유는 훈련중 셀을 실행하면 loss_plot 배열이 리셋되기 때문이다.
    loss_plot = []

    @tf.function
    def train_step(img_tensor, target):
        loss = 0
        # decoder.reset_state는 위에서 정의했음. 같은 shape로 0으로 만들어주는 함수.
        # batch_size에 타겟의 shape를 넣으면 같은형상의 0 행렬로 변환
        # 매 hidden state마다 실행하는데 캡션은 이미지간에 관련이 없기 때문이다.
        hidden = decoder.reset_state(batch_size=target.shape[0])
        dec_input = tf.expand_dims(
            [tokenizer.word_index['<start>']] * target.shape[0], 1)

        with tf.GradientTape() as tape:
            # 아까 정의한 CNN encoder를 실행하는 부분
            features = encoder(img_tensor)
            for i in range(1, target.shape[1]):
                # 아까 RNN decoder에서 정의한 디코더를 실행하는 부분
                predictions, hidden, _ = decoder(dec_input, features, hidden)
                loss += loss_function(target[:, i], predictions)
                # using teacher forcing
                dec_input = tf.expand_dims(target[:, i], 1)
        total_loss = (loss / int(target.shape[1]))
        trainable_variables = encoder.trainable_variables + decoder.trainable_variables
        gradients = tape.gradient(loss, trainable_variables)
        optimizer.apply_gradients(zip(gradients, trainable_variables))

        return loss, total_loss

    EPOCHS = 1
    for epoch in range(start_epoch, EPOCHS):
        start = time.time()
        total_loss = 0
        for (batch, (img_tensor, target)) in enumerate(dataset):
            # 훈련부분. train_step의 batch_loss와 t_loss 저장
            batch_loss, t_loss = train_step(img_tensor, target)
            total_loss += t_loss
        # storing the epoch end loss value to plot later
        loss_plot.append(total_loss / num_steps)
        if epoch % 5 == 0:
            ckpt_manager.save()

    def evaluate(image):
        # 0 행렬로 초기화
        attention_plot = np.zeros((max_length, attention_features_shape))
        # decode.reset_state로 초기값으로 지정해줌
        hidden = decoder.reset_state(batch_size=1)

        temp_input = tf.expand_dims(load_image(image)[0], 0)
        img_tensor_val = image_features_extract_model(temp_input)
        img_tensor_val = tf.reshape(
            img_tensor_val, (img_tensor_val.shape[0], -1, img_tensor_val.shape[3]))
        # CNN encoder로 마무리
        features = encoder(img_tensor_val)
        dec_input = tf.expand_dims([tokenizer.word_index['<start>']], 0)
        result = []
        for i in range(max_length):
            # decoder로 캡션 생성하는 부분
            predictions, hidden, attention_weights = decoder(
                dec_input, features, hidden)
            attention_plot[i] = tf.reshape(attention_weights, (-1, )).numpy()
            predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
            result.append(tokenizer.index_word[predicted_id])
            if tokenizer.index_word[predicted_id] == '<end>':
                return result, attention_plot
            dec_input = tf.expand_dims([predicted_id], 0)
        attention_plot = attention_plot[:len(result), :]
        return result, attention_plot

    # captions on the validation set
    rid = np.random.randint(0, len(img_path_val))
    image = img_path_val[rid]
    real_caption = ' '.join([tokenizer.index_word[i]
                             for i in cap_val[rid] if i not in [0]])
    # 이미지 평가부
    result, attention_plot = evaluate(image)

    # 이미지 url은 practice에 해당 이미지 파일을 저장 후 다음 경로에 넣고 실행하면 된다.
    # ex) image_url = './practice/02.jpg'

    # image_url = UPLOAD_DIR + '\\imageCaptioning\\static\\' + HttpImagePath
    image_url = UPLOAD_DIR + '\\static\\' + HttpImagePath

    image_extension = image_url[-4:]
    result, attention_plot = evaluate(image_url)
    return ' '.join(result)
