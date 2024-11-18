import argparse
import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help'
)
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=5000)
parser.add_argument('--images', default='./static/images')
parser.add_argument('--output', default='test.csv')
args = parser.parse_args()
# Список изображений с именами файлов из папки static/images
images = os.listdir(args.images)
# Словарь для хранения описаний для каждого изображения
descriptions = {}


@app.route('/image/<int:image_index>', methods=['GET', 'POST'])
def image(image_index):
    with open(args.output) as lists:
        capt = pd.read_csv(lists)
    while sum(images[image_index] == capt['image']):
        image_index += 1
    # Если форма отправлена, сохранить описание
    if request.method == 'POST':
        print(images[image_index])
        # return redirect(url_for('image', image_index=image_index))
        description = request.form.get('description')
        descriptions[image_index] = description
        with open(args.output11, 'a') as file:
            if description:
                file.write(f'{images[image_index]},{description}\n')
        # Переход к следующему изображению или окончание
        if image_index + 1 < len(images):
            return redirect(url_for('image', image_index=image_index + 1))
        else:
            return redirect(url_for('validate', 0))  # В конце перейти на страницу с результатами

    # Отображаем текущее изображение
    image_url = url_for(args.images, filename=f'{images[image_index]}')

    return render_template('image.html', image_url=image_url, image_index=image_index)


@app.route('/')
def index():
    # Перенаправление на первое изображение
    return redirect(url_for('image', image_index=0))


@app.route('/validate/<int:image_index>', methods=['GET', 'POST'])
def validate(image_index: int):
    df = pd.read_csv(args.output)
    if request.method == 'POST':
        print(images[image_index])
        # return redirect(url_for('image', image_index=image_index))
        description = request.form.get('description')
        descriptions[image_index] = description
        if description != (df[df['image'] == images[image_index]]['captcha']).values[0]:
            df['image'][images[image_index]] = description
            df.to_csv(args.output, index=False)
        # Переход к следующему изображению или окончание
        if image_index + 1 < len(images):
            return redirect(url_for('validate', image_index=image_index + 1))
        else:
            return redirect(url_for('summary'))  # В конце перейти на страницу с результатами

    # Отображаем текущее изображение
    image_url = url_for(args.images, filename=f'{images[image_index]}')
    value = (df[df['image'] == images[image_index]]['captcha']).values[0]
    print(value)
    return render_template('validate.html', image_url=image_url, image_index=image_index, value=value)


if __name__ == '__main__':
    app.run(host=args.host, port=args.port, debug=True)
