import cv2

face_cascade_path = '../cascade_classifier/haarcascade_frontalface_default.xml'
eye_cascade_path = '../cascade_classifier/haarcascade_eye.xml'

face_cascade = cv2.CascadeClassifier(face_cascade_path)  # 顔検出の分類器
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)  # 目検出の分類器


def show_detected_face(img):
    # 画像をグレースケールに変換（学習済みのモデルがグレースケールでの検出前提だから）
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces: 検出した部分の座標を返すイテレーター
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in faces:
        # 画面上に描画
        cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
        face = img[y: y + h, x: x + w]
        face_gray = img_gray[y: y + h, x: x + w]
        eyes = eye_cascade.detectMultiScale(face_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            print(ex, ey, ew, eh)
            print(type(img))


def face_detect_from_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        print(type(img))
        show_detected_face(img)
        cv2.imshow('video image', img)
        key = cv2.waitKey(10)
        if key == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()


def face_detector_from_src(src: str):
    img = cv2.imread(src)
    show_detected_face(img)


if __name__ == '__main__':
    face_detect_from_webcam()
