import os
from flask import Flask, render_template, request, redirect, url_for
from withoutLibCBC import *
from encByLib import *
from crypoTest import *

UPLOAD_FOLDER = 'static/tmpImg'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file.filename = 'originalImg.png'

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            key = int(request.form.get('key'))
            iv = int(request.form.get('iv'))
            key_length = int(int(request.form.get('key_length'))/8)

            origFN = 'originalImg.png'
            path = "static/tmpImg/"

            try:
                encByLibRun(path, origFN, key, iv, key_length)
                encAndDecRun(path, origFN, key, iv, key_length)
            except Exception as e:
                return redirect(url_for('error', message='Ошибка при шифровании/расшифровании изображения:/n' + str(e)))

            return redirect('/encImage')
    return render_template('index.html')


@app.route('/encImage')
def encImage():
    # Получаем пути к зашифрованным картинкам
    encrypted_image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encryptedImg.png')
    encrypted_image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encByLibImg.png')
    orig_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'originalImg.png')
    # Выполняем расчеты
    entropy_value1 = calculate_entropy(Image.open(encrypted_image1_path), size=100 * 100)
    entropy_value2 = calculate_entropy(Image.open(encrypted_image2_path), size=100 * 100)
    uaci_value = get_uaci(orig_image_path, encrypted_image1_path)
    npcr_value = get_npcr(orig_image_path, encrypted_image1_path)
    uaci_value2 = get_uaci(orig_image_path, encrypted_image2_path)
    npcr_value2 = get_npcr(orig_image_path, encrypted_image2_path)
    avg_brightness1 = get_avg_brightness(encrypted_image1_path)
    avg_brightness2 = get_avg_brightness(encrypted_image2_path)
    coff_corelation1 = get_coff_corelation(encrypted_image1_path)
    coff_corelation2 = get_coff_corelation(encrypted_image2_path)

    # Выводим результаты на странице
    return render_template('encImage.html', entropy_value1=entropy_value1, entropy_value2=entropy_value2, uaci_value=uaci_value, npcr_value=npcr_value, uaci_value2=uaci_value2, npcr_value2=npcr_value2, avg_brightness1=avg_brightness1, avg_brightness2=avg_brightness2, coff_corelation1=coff_corelation1, coff_corelation2=coff_corelation2)


@app.route('/error')
def error():
    message = request.args.get('message')
    return render_template('error.html', message=message)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
