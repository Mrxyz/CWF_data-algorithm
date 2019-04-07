from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from process import process_text, ranking
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt'])


# 判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 文档结构化
@app.route('/api/struct', methods=['POST'], strict_slashes=False)
def struct_process():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        f.save(os.path.join(file_dir, fname))  # 保存文件到upload目录
        result = json.dumps(process_text(fname), ensure_ascii=False)
        return result
    else:
        return jsonify({"code": 1001, "errmsg": "上传失败"})


# 班级排序
@app.route("/api/rank", methods=['POST'],strict_slashes=False)
def rank():
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        rank = ranking(process_text(fname))
        return jsonify(rank)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)