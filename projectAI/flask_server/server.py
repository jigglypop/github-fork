import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_restful import reqparse
from flask_cors import CORS
# 모듈 임포트
from SentimentAnalysis.run import SentimentAnalysis
from imageCaptioning.run import ImageCaption
from StyleTransfer.run import StyleTransfer
from ImageNet.run import ImageNet
import json

# 업로드 폴더가 있는 절대경로를 받아온다.
UPLOAD_DIR = os.getcwd()
# 플라스크 서버 시작
app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR + '\\static\\'
# CORS
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})

# 이미지 캡셔닝
@app.route('/images', methods=['POST'])
def images_main():
    f = request.files['photo']
    fname = secure_filename(f.filename)
    path = os.path.join(app.config['UPLOAD_DIR'], fname)
    f.save(path)
    result = ImageCaption(fname)
    return jsonify(path="http://127.0.0.1:5000/static/" + fname, caption=result)

# 스타일 트랜스퍼
@app.route('/styletransfer', methods=['POST'])
def styletransfer_main():
    # content 저장
    content = request.files['content']
    content_name = secure_filename(content.filename)
    content_path = os.path.join(
        app.config['UPLOAD_DIR']+"styletransfer\\", content_name)
    content.save(content_path)

    # style 저장
    style = request.files['style']
    style_name = secure_filename(style.filename)
    style_path = os.path.join(
        app.config['UPLOAD_DIR']+"styletransfer\\", style_name)
    style.save(style_path)

    # styletransfer 실행
    result = StyleTransfer(content_path, style_path)
    return jsonify(path="http://127.0.0.1:5000/static/styletransfer_result/" + result)

# 감정 분석
@app.route('/sent', methods=['POST'])
def sent_main():
    text = request.json['text']
    negative, positive = SentimentAnalysis(text)
    return jsonify(positive=positive, negative=negative)

# 이미지넷
@app.route('/imagenet', methods=['POST'])
def imagenet_main():
    imagenet = request.files['imagenet']
    imagenet_name = secure_filename(imagenet.filename)
    imagenet_path = os.path.join(
        app.config['UPLOAD_DIR']+"imagenet\\", imagenet_name)
    imagenet.save(imagenet_path)
    data = ImageNet(imagenet_path)
    return jsonify(path="http://127.0.0.1:5000/static/imagenet/" + imagenet_name, data=data)


# 서버 시작
if __name__ == '__main__':
    app.run(debug=True)
