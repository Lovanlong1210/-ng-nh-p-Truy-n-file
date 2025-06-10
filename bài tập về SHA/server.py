from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import hashlib
import os

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' # Consider a more secure key for production
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
socketio = SocketIO(app, cors_allowed_origins="*") # Allow all origins for simplicity in development

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('upload_start')
def handle_upload_start(data):
    filename = data['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Store file data in a temporary buffer or directly write to a temp file
    # For simplicity, we'll assume small files for now and accumulate in memory
    # For larger files, a more robust chunking and writing mechanism is needed
    if 'files_in_progress' not in app.config:
        app.config['files_in_progress'] = {}
    app.config['files_in_progress'][filename] = {
        'buffer': b'',
        'hash_calculator': hashlib.sha256()
    }
    emit('upload_ready', {'filename': filename})

@socketio.on('upload_chunk')
def handle_upload_chunk(data):
    filename = data['filename']
    chunk = data['chunk']
    is_last_chunk = data['is_last_chunk']

    if filename in app.config.get('files_in_progress', {}):
        file_data = app.config['files_in_progress'][filename]
        decoded_chunk = bytes(chunk)
        file_data['buffer'] += decoded_chunk
        file_data['hash_calculator'].update(decoded_chunk)

        if is_last_chunk:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, 'wb') as f:
                f.write(file_data['buffer'])
            
            calculated_hash = file_data['hash_calculator'].hexdigest()
            # Clean up temporary data
            del app.config['files_in_progress'][filename]
            
            emit('upload_complete', {'filename': filename, 'hash': calculated_hash, 'status': 'success'})
            print(f"File {filename} uploaded. SHA256: {calculated_hash}")
        else:
            emit('chunk_received', {'filename': filename, 'status': 'progress'})


@socketio.on('download_request')
def handle_download_request(data):
    filename = data['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                while True:
                    bytes_read = f.read(4096)
                    if not bytes_read:
                        break
                    sha256_hash.update(bytes_read)
                    emit('download_chunk', {'filename': filename, 'chunk': list(bytes_read)})
            emit('download_complete', {'filename': filename, 'hash': sha256_hash.hexdigest(), 'status': 'success'})
            print(f"File {filename} sent for download. SHA256: {sha256_hash.hexdigest()}")
        except Exception as e:
            emit('download_error', {'filename': filename, 'message': str(e), 'status': 'error'})
            print(f"Error sending file {filename}: {e}")
    else:
        emit('download_error', {'filename': filename, 'message': 'File not found', 'status': 'error'})
        print(f"File {filename} not found for download.")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 