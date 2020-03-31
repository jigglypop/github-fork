from tensorflow.keras.applications import MobileNetV2
import tensorflow as tf
import numpy as np
import tensorflow_hub as hub
import cv2
import os


def ImageNet(imagenet_path):
    mobile_net_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"
    model = tf.keras.Sequential([
        hub.KerasLayer(handle=mobile_net_url, input_shape=(
            224, 224, 3), trainable=False)
    ])

    mobilev2 = MobileNetV2()
    # tf.keras.utils.plot_model(mobilev2)
    label_file = tf.keras.utils.get_file('label', './label')
    label_text = None
    with open(label_file, 'r') as f:
        label_text = f.read().split('\n')[:-1]

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    # MobileNet을 이용한 예측
    img = cv2.imread(imagenet_path)
    img = cv2.resize(img, dsize=(224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    logits = model.predict(img)[0]
    prediction = softmax(logits)

    # 가장 높은 확률의 예측값 5개를 뽑음
    top_5_predict = prediction.argsort()[::-1][:5]
    labels = [label_text[index] for index in top_5_predict]

    # color = color[::-1]
    pre = list(prediction[top_5_predict][::-1] * 100)
    lab = list(labels[::-1])
    results = dict()
    # for i in range(5):
    #     results[f'{i+1}: {lab[4-i]}'] = str(pre[4-i])
    for i in range(5):
        results[i+1] = {'name': lab[4-i], 'persent': str(pre[4-i])}
    return results
