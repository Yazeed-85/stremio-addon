from flask import Flask, jsonify, request, render_template_string, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# استخدام مجلد /tmp الخاص بـ Render للملفات المؤقتة
UPLOAD_FOLDER = '/tmp'

MANIFEST = {
    "id": "org.yzads.local.cloud.fixed",
    "version": "4.0.0",
    "name": "YZ Local Subs (PRO)",
    "description": "نسخة يزيد الاحترافية - تصميم جديد وإصلاح للروابط",
    "resources": ["subtitles"],
    "types": ["movie", "series"],
    "idPrefixes": ["tt"]
}

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

# واجهة المستخدم الاحترافية (Dark Mode & Modern UI)
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YZ Subs Dashboard</title>
            <style>
                body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .card { background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; width: 90%; max-width: 400px; }
                h1 { color: #38bdf8; margin-bottom: 10px; font-size: 24px; }
                p { color: #94a3b8; font-size: 14px; margin-bottom: 30px; }
                input[type="file"] { display: none; }
                .custom-file-upload { border: 2px dashed #38bdf8; display: inline-block; padding: 20px; cursor: pointer; border-radius: 12px; margin-bottom: 20px; transition: 0.3s; width: 100%; box-sizing: border-box; }
                .custom-file-upload:hover { background: #0c4a6e; }
                .btn { background: #38bdf8; color: #0f172a; border: none; padding: 12px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; transition: 0.3s; }
                .btn:hover { background: #0ea5e9; transform: translateY(-2px); }
                .footer { margin-top: 20px; font-size: 12px; color: #475569; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>YZ Subs (PRO)</h1>
                <p>مرحباً يزيد! ارفع ملف SRT وابدأ المشاهدة</p>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <label class="custom-file-upload">
                        <input type="file" name="file" accept=".srt"/>
                        <span>📁 اختر ملف الترجمة</span>
                    </label>
                    <button type="submit" class="btn">تحديث الترجمة الآن 🚀</button>
                </form>
                <div class="footer">متصل بـ Render Cloud ☁️</div>
            </div>
        </body>
        </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "<h1>خطأ: اختر ملفاً أولاً!</h1>"
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, 'sub.srt'))
    return '''
        <div style="background:#0f172a; color:white; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:sans-serif;">
            <h1 style="color:#22c55e;">تم الرفع بنجاح! ✅</h1>
            <p>اذهب لستريميو الآن واختر "Arabic (Cloud) ☁️"</p>
            <a href="/" style="color:#38bdf8; text-decoration:none;">رفع ملف آخر</a>
        </div>
    '''

@app.route('/subtitles/<path:rest>')
def subtitles(rest):
    # إجبار الرابط على استخدام HTTPS لضمان عدم رفضه من المتصفح أو التطبيق
    base_url = request.host_url.replace("http://", "https://")
    return jsonify({
        "subtitles": [{
            "id": "yz-cloud-pro",
            "url": f"{base_url}static/sub.srt",
            "lang": "Arabic (Cloud) ☁️"
        }]
    })

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(UPLOAD_FOLDER, path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
