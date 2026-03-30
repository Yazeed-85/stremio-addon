from flask import Flask, jsonify, request, render_template_string, Response
from flask_cors import CORS
import os

app = Flask(__name__)
# تفعيل CORS لضمان قبول تطبيق ستريميو للترجمة
CORS(app, resources={r"/*": {"origins": "*"}})

# قاعدة بيانات وهمية في الذاكرة لتخزين محتوى الترجمة ورابط آخر ملف
db = {
    "subtitle_content": "",
    "current_sub_url": ""
}

MANIFEST = {
    "id": "org.yzads.cloud.memory",
    "version": "5.0.0",
    "name": "YZ Subs (In-Memory PRO)",
    "description": "نسخة يزيد الاحترافية - تخزين ذكي في الذاكرة لإصلاح مشاكل التحميل",
    "resources": ["subtitles"],
    "types": ["movie", "series"],
    "idPrefixes": ["tt"]
}

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

@app.route('/')
def index():
    # الواجهة الاحترافية الـ Dark Mode
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YZ Subs Dashboard (Memory)</title>
            <style>
                body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .card { background: #1e293b; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #334155; width: 90%; max-width: 400px; }
                h1 { color: #38bdf8; font-size: 24px; }
                p { color: #94a3b8; font-size: 14px; margin-bottom: 30px; }
                input[type="file"] { display: none; }
                .custom-file-upload { border: 2px dashed #38bdf8; display: inline-block; padding: 20px; cursor: pointer; border-radius: 12px; margin-bottom: 20px; transition: 0.3s; width: 100%; box-sizing: border-box; }
                .custom-file-upload:hover { background: #0c4a6e; }
                .btn { background: #38bdf8; color: #0f172a; border: none; padding: 12px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; transition: 0.3s; }
                .btn:hover { background: #0ea5e9; transform: translateY(-2px); }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>YZ Subs (Memory)</h1>
                <p>مرحباً يزيد! هذه النسخة تخزن الترجمة في الذاكرة لضمان العمل</p>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <label class="custom-file-upload">
                        <input type="file" name="file" accept=".srt"/>
                        <span>📁 اختر ملف SRT الجديد</span>
                    </label>
                    <button type="submit" class="btn">تحديث الترجمة الآن 🚀</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "<h1>خطأ: اختر ملفاً أولاً!</h1>"
    
    file = request.files['file']
    # قراءة محتوى الملف كص ورقة وتخزينه في الذاكرة
    try:
        content = file.read().decode('utf-8', errors='replace')
        db["subtitle_content"] = content
        # تحديث الرابط الفريد لملف الترجمة لضمان تجاوز الكاش في ستريميو
        import time
        db["current_sub_url"] = f"sub_{int(time.time())}.srt"
    except Exception as e:
        return f"<h1>حدث خطأ في قراءة الملف: {str(e)}</h1>"
    
    return '''
        <div style="background:#0f172a; color:white; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:sans-serif;">
            <h1 style="color:#22c55e;">تم الرفع للذاكرة بنجاح! ✅</h1>
            <p>اذهب لستريميو الآن واختر "Arabic (Memory) ☁️"</p>
            <a href="/" style="color:#38bdf8; text-decoration:none;">رفع ملف آخر</a>
        </div>
    '''

@app.route('/subtitles/<path:rest>')
def subtitles(rest):
    # إجبار الرابط على استخدام HTTPS
    base_url = request.host_url.replace("http://", "https://")
    
    # إذا لم يتم رفع أي ترجمة، نرسل رد فارغ
    if not db["subtitle_content"]:
        return jsonify({"subtitles": []})

    # نرسل رابط ديناميكي يؤدي إلى دالة get_subtitle_file
    return jsonify({
        "subtitles": [{
            "id": "yz-memory-sub",
            "url": f"{base_url}{db['current_sub_url']}",
            "lang": "Arabic (Memory) ☁️"
        }]
    })

# دالة لخدمة ملف الترجمة مباشرة من الذاكرة
@app.route('/<filename>')
def get_subtitle_file(filename):
    if filename == db["current_sub_url"] and db["subtitle_content"]:
        # نرسل محتوى النص مع نوع MIME الصحيح للترجمة
        return Response(
            db["subtitle_content"],
            mimetype='text/plain',
            headers={'Content-Disposition': 'inline; filename=sub.srt'}
        )
    return "File Not Found", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
