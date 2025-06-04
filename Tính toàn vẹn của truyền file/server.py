from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import hashlib
import json
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Cấu hình thư mục upload
UPLOAD_FOLDER = 'uploads'
USERS_FILE = 'users.json'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Đọc thông tin người dùng từ file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "admin": {
            "password": "admin123",
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
    }

# Lưu thông tin người dùng vào file
def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Khởi tạo danh sách người dùng
USERS = load_users()

# Lưu trữ thông tin file
files = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Vui lòng nhập đầy đủ thông tin"
        })
    
    if username in USERS:
        return jsonify({
            "status": "error",
            "message": "Tên đăng nhập đã tồn tại"
        })
    
    # Thêm người dùng mới
    USERS[username] = {
        "password": password,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    save_users(USERS)
    
    return jsonify({
        "status": "success",
        "message": "Đăng ký thành công"
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and USERS[username]['password'] == password:
        # Cập nhật thời gian đăng nhập
        USERS[username]['last_login'] = datetime.now().isoformat()
        save_users(USERS)
        return jsonify({
            "status": "success",
            "message": "Đăng nhập thành công"
        })
    return jsonify({
        "status": "error",
        "message": "Sai tên đăng nhập hoặc mật khẩu"
    })

@app.route('/list_users', methods=['GET'])
def list_users():
    return jsonify(list(USERS.keys()))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    
    file = request.files['file']
    sender = request.form.get('sender')
    receiver = request.form.get('receiver')
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Tính toán SHA-256
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        sha256 = sha256_hash.hexdigest()
        
        # Lưu thông tin file
        file_info = {
            "name": filename,
            "sha256": sha256,
            "sender": sender,
            "receiver": receiver,
            "upload_time": datetime.now().isoformat()
        }
        files.append(file_info)
        
        return jsonify({
            "status": "uploaded",
            "sha256": sha256
        })

@app.route('/list_files', methods=['GET'])
def list_files():
    return jsonify(files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
