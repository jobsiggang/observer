from flask import Flask, render_template
from views import cv_views
import cv2

app = Flask(__name__)
app.register_blueprint(cv_views.bp)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
