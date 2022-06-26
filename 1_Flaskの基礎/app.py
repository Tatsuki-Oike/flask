from flask import Flask, render_template, url_for, request, redirect, session, flash

app = Flask(__name__)

# 基本
@app.route('/')
def hello():
    return 'FlaskでWebアプリ作成'

# 1_1_htmlファイルを表示
@app.route('/html')
def html():
    return render_template('1_1_index.html')

# 1_2_cssファイルを表示
@app.route('/css')
def css():
    return render_template('1_2_css.html')

# 1_3layoutの利用
@app.route('/layout')
def layout():
    return render_template('1_3_layout_sample.html')

# 1_4_値の受け渡し
@app.route('/value')
def value():
    return render_template('1_4_value.html', title='値の受け渡し', content='ここに内容')

@app.route('/value/<title>/<content>')
def value_query(title, content):
    return render_template('1_4_value.html', title=title, content=content)

# 2_1_formの利用
@app.route('/form', methods=['GET'])
def form_get():
    return render_template('2_1_form.html', content='ここの文章が変わるよ')

@app.route('/form', methods=['POST'])
def form_post():
    text_input = request.form['t']
    return render_template('2_1_form.html', content=f'「{text_input}」が入力されたよ')

# 2_2_statement
@app.route('/statement', methods=['GET'])
def statement_get():
    return render_template('2_2_statement.html')

@app.route('/statement', methods=['POST'])
def statement_post():
    post = True
    n = 10
    data = ["data0", "data1", "data2", "data3", "data4"]
    return render_template('2_2_statement.html', number=n, data=data, post=post)

# 2_3_flash
@app.route('/flash', methods=['GET'])
def flash_get():
    return render_template('2_3_flash.html')

@app.route('/flash', methods=['POST'])
def flash_post():
    
    # 入力受け取り
    t = request.form['t']
    n = request.form['n']
    
    # Flashの設定
    input_flg = True
    
    if not t:
        flash("テキストを入力してください")
        input_flg = False
        
    if not n:
        flash("数値を入力してください")
        input_flg = False
        
    if not input_flg:
        return redirect(url_for("flash_get"))
    
    post = True
    
    return render_template('2_3_flash.html', text=t, number=int(n), post=post)

# 2_4_セッションの利用とリダイレクト
app.config["SECRET_KEY"] = "jfaogiehi2iw8jLD0ejJ"

@app.route('/session', methods=['GET'])
def session_get():
    if "text_input" in session:
        text_input = session["text_input"]
        content = f'「{text_input}」が入力されたよ'
    else:
        content = 'ここの文章が変わるよ'
    return render_template('2_4_session.html', title='sessionの利用', content=content)

@app.route('/session', methods=['POST'])
def session_post():
    session["text_input"] = request.form['t']
    return redirect("/session")

# 3_1_フィルター
@app.route('/filter', methods=['GET'])
def filter_get():
    return render_template('3_1_filter.html', text="", number=0)

@app.route('/filter', methods=['POST'])
def filter_post():
    t = request.form['t']
    n = request.form['n']
    if not n:
        n = 0
    return render_template('3_1_filter.html', text=t, number=int(n))

app.template_filter('square')
def square_filter(x):
    y = x**2
    return y

app.jinja_env.filters['square'] = square_filter

# 3_2_コンテクスト・プロセッサ
@app.route('/cp', methods=['GET'])
def cp_get():
    return render_template('3_2_cp.html', number=0)

@app.route('/cp', methods=['POST'])
def cp_post():
    n = request.form['n']
    if not n:
        n = 0
    return render_template('3_2_cp.html', number=int(n))

@app.context_processor
def sample_processor():
    def square_func(x):
        y = x**2
        return y
    return dict(square=square_func)

# 3_3_関数の利用
@app.route('/function', methods=['GET'])
def function_get():
    return render_template('3_3_function.html', number=0, y=0)

@app.route('/function', methods=['POST'])
def function_post():
    n = request.form['n']
    if not n:
        n = 0
    else:
        n = int(n)
    y = square_f(n)
    return render_template('3_3_function.html', number=n, y=y)

def square_f(x):
    y = x**2
    return y

# 3_4_モジュールの利用
from function import square

@app.route('/module', methods=['GET'])
def module_get():
    return render_template('3_4_module.html', number=0, y=0)

@app.route('/module', methods=['POST'])
def module_post():
    n = request.form['n']
    if not n:
        n = 0
    else:
        n = int(n)
    y = square.square_function(n)
    return render_template('3_4_module.html', number=n, y=y)

# 4_1_画像の表示
import cv2
import shutil

@app.route('/image', methods=['GET'])
def image_get():
    return render_template('4_1_image.html')

@app.route('/image', methods=['POST'])
def image_post():
    
    # ファイルの作成
    img_dir = "static/images/"
    
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
        
    os.makedirs(img_dir, exist_ok=True)
    
    # 入力受け取り
    input_image = request.files['image']
    
    # Flashの設定
    input_flg = True
    
    if not input_image:
        flash("画像を入力してください")
        input_flg = False
        
    if not input_flg:
        return redirect(url_for("image_post"))
    
    # 画像変換
    stream = input_image.stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)
    
    # 画像保存
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    img_path = img_dir + dt_now + ".jpg"
    cv2.imwrite(img_path, img)
    
    return render_template('4_1_image.html', content=img_path)

# 4_2_プロット1
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import datetime

@app.route('/plot1')
def plot1():
    
    # ファイルの作成
    img_dir = "static/images/"
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
    os.makedirs(img_dir, exist_ok=True)
    
    # 画像の保存先決定
    dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    img_path = img_dir + dt_now + ".png"
    
    # プロットの作成と保存
    x = np.linspace(0, 10, 100)
    y = np.cos(x)
    plt.cla()
    plt.plot(x, y)
    plt.savefig(img_path)
    
    return render_template('4_2_plot.html', url =img_path)

# 4_3_プロット2
import base64
from io import BytesIO

@app.route("/plot2")
def plot2():
    
    # プロットの作成
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.cla()
    plt.plot(x, y)
    
    # 変換
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return render_template("4_3_plot.html", img=data)

if __name__ == '__main__':
    app.run(debug=True)