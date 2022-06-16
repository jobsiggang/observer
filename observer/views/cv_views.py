from flask import render_template, Response, Blueprint, send_file
from datetime import datetime
import cv2

bp = Blueprint('cv_views', __name__, url_prefix='/')


@bp.route('/stream')
def stream():
    return render_template('stream.html')


camera = cv2.VideoCapture(0)#외장카메라면 1로


def gen_frames():
    while True:
        success, frame = camera.read()  # 카메라프레임읽기
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/capture')
def capture():
    # 이미지 저장하는 함수
    ret, img = camera.read()
    if ret:
        id = datetime.now().strftime("%y%m%d%H%M%S")
        file_path = "./static/images/capture.png"
        file_name = "img"+id+".png"
        cv2.imwrite(file_path, img)
    return send_file(file_path, mimetype='image/png', as_attachment=True, attachment_filename=file_name)
