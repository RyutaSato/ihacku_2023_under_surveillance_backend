import cv2
import numpy as np
from flask import Flask, request
from flask_socketio import SocketIO, send
from face_detector import show_detected_face

app = Flask(__name__)
socketio = SocketIO(app)
namespace = "/ws"

@socketio.on('connect', namespace)
def on_connect():
    print('WebSocket connected')


@socketio.on('disconnect', namespace)
def on_disconnect():
    print('WebSocket disconnected')

@socketio.on('message', namespace)
def on_stream(msg: str):
    data = bytes(msg)
    # EOIマーカーの位置を検索
    end: int = data.find(b'\xff\xd9')

    # EOIマーカーが見つかった場合
    if end != -1:
        # JPEG画像のバイナリデータを取得
        frame_data = data[:end + 2]

        # バイナリデータから画像を読み込む
        img = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
        if show_detected_face(img, is_gray=True):
            socketio.send({"face": True}, json=True)



if __name__ == '__main__':
    socketio.run(app)
