from flask import Flask, jsonify, request, render_template_string, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/tmp' # في Render يفضل استخدام /tmp للملفات المؤقتة

MANIFEST = {
    "id": "org.yzads.local.cloud",
    "version": "3.0.0",
    "name": "YZ Cloud Subs",
    "description": "اضافة يزيد لرفع الترجمة - تعمل من السحاب!",
    "resources": ["subtitles"],
    "types": ["movie", "series"],
    "idPrefixes": ["tt"]
}

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

@app.route('/')
def index():
    return render_template_string('''
        <div style="text-align:center; padding:50px; font-family:Arial;">
            <h1 style="color:#2c3e50;">مرحباً يزيد! ارفع ملف الترجمة هنا</h1>
            <p>هذه النسخة تعمل من السحاب 24 ساعة</p>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".srt">
                <br><br>
                <input type="submit" value="تحديث الترجمة في ستريميو 🚀" style="padding:10px 20px; background:#e74c3c; color:white; border:none; border-radius:5px; cursor:pointer;">
            </form>
        </div>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "<h1>خطأ: لم تختر ملفاً!</h1><a href='/'>ارجع</a>"
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, 'sub.srt'))
    return "<h1>تم الرفع بنجاح! ✅</h1><p>اذهب لستريميو الآن.</p><a href='/'>رفع ملف آخر</a>"

@app.route('/subtitles/<path:rest>')
def subtitles(rest):
    # نستخدم الرابط الجديد الخاص بموقع Render لاحقاً
    host_url = request.host_url
    return jsonify({
        "subtitles": [{
            "id": "yz-cloud",
            "url": f"{host_url}static/sub.srt",
            "lang": "Arabic (Cloud) ☁️"
        }]
    })

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(UPLOAD_FOLDER, path)

if __name__ == '__main__':
    # هذا السطر مهم جداً لـ Render ليعرف المنفذ المفتوح
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)