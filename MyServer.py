from flask import Flask, render_template, request
import os
import Label  # Detect Label 관련 라이브러리
import Compare  # 얼굴 비교 라이브러리
from werkzeug.utils import secure_filename

app = Flask(__name__)

if not os.path.exists('static/imgs'):
    os.mkdir('static/imgs')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    num1 = int(request.args.get('num1', 0))
    num2 = int(request.args.get('num2', 0))
    s = '{} + {} = {}'.format(num1, num2, num1 + num2)
    return s

@app.route('/label', methods=['POST'])
def label():
    if request.method == 'POST':
        f = request.files['label']
        filename = secure_filename(f.filename)
        f.save('static/imgs/' + filename)

        r = 'static/imgs/' + filename
        result = Label.detect_labels_local_file(r)
        return result

@app.route('/compare', methods=['POST'])
def compare():
    if request.method == 'POST':
        f1 = request.files['face1']
        f2 = request.files['face2']

        filename1 = secure_filename(f1.filename)
        filename2 = secure_filename(f2.filename)

        f1.save('static/imgs/' + filename1)
        f2.save('static/imgs/' + filename2)

        r1 = 'static/imgs/' + filename1
        r2 = 'static/imgs/' + filename2

        result = Compare.compare_faces(r1, r2)
        return result

if __name__ == '__main__':
    app.run()
