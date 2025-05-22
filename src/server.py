from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.json_utils import load_tasks, save_tasks, load_keys
from config import DOWNLOAD_DIR
import src.yt_handler as yt_handler
import src.auth as auth
import random
import string
import os
import json
import sqlite3
from datetime import datetime
import base64, hashlib
from Crypto.Cipher import AES

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Allow all origins
app.json.sort_keys = False

def generate_random_id(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/get_video', methods=['POST'])
@auth.check_api_key('get_video')
def get_video():
    data = request.json
    url = data.get('url')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    force_keyframes = data.get('force_keyframes')
    video_format = data.get('video_format', 'bestvideo')
    audio_format = data.get('audio_format', 'bestaudio')
    
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required'}), 400
    
    task_id = generate_random_id()
    tasks = load_tasks()
    tasks[task_id] = {
        'key_name': auth.get_key_name(request.headers.get('X-API-Key')),
        'status': 'waiting',
        'task_type': 'get_video',
        'url': url,
        'start_time': start_time,
        'end_time': end_time,
        'force_keyframes': force_keyframes,
        'video_format': video_format,
        'audio_format': audio_format
    }
    save_tasks(tasks)

    return jsonify({'status': 'waiting', 'task_id': task_id})

@app.route('/get_audio', methods=['POST'])
@auth.check_api_key('get_audio')
def get_audio():
    data = request.json
    url = data.get('url')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    force_keyframes = data.get('force_keyframes')
    video_format = data.get('video_format', 'bestvideo')
    audio_format = data.get('audio_format', 'bestaudio')
    
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required'}), 400
    
    task_id = generate_random_id()
    tasks = load_tasks()
    tasks[task_id] = {
        'key_name': auth.get_key_name(request.headers.get('X-API-Key')),
        'status': 'waiting',
        'task_type': 'get_audio',
        'url': url,
        'start_time': start_time,
        'end_time': end_time,
        'force_keyframes': force_keyframes,
        'video_format': video_format,
        'audio_format': audio_format
    }
    save_tasks(tasks)

    return jsonify({'status': 'waiting', 'task_id': task_id})

@app.route('/get_info', methods=['POST'])
@auth.check_api_key('get_info')
def get_info():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required'}), 400
    
    task_id = generate_random_id()
    # keys = load_keys()
    # key_name = auth.get_key_name(request.headers.get('X-API-Key'))
    # key_info = keys[key_name]

    # if 'task_ids' not in key_info:
    #     key_info['task_ids'] = []
    # key_info['task_ids'].append(task_id)
    # keys[key_name] = key_info
    # auth.save_keys(keys)
    
    tasks = load_tasks()
    tasks[task_id] = {
        'key_name': auth.get_key_name(request.headers.get('X-API-Key')),
        'status': 'waiting',
        'task_type': 'get_info',
        'url': url
    }
    save_tasks(tasks)

    return jsonify({'status': 'waiting', 'task_id': task_id})

@app.route('/get_live_video', methods=['POST'])
@auth.check_api_key('get_live_video')
def get_live_video():
    data = request.json
    url = data.get('url')
    start = data.get('start', 0)
    duration = data.get('duration')
    video_format = data.get('video_format', 'bestvideo')
    audio_format = data.get('audio_format', 'bestaudio')
    
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required'}), 400
    
    task_id = generate_random_id()
    # keys = load_keys()
    # key_name = auth.get_key_name(request.headers.get('X-API-Key'))
    # key_info = keys[key_name]
    # keys[key_name] = key_info
    # auth.save_keys(keys)

    # if 'task_ids' not in key_info:
    #     key_info['task_ids'] = []
    # key_info['task_ids'].append(task_id)

    tasks = load_tasks()
    tasks[task_id] = {
        'key_name': auth.get_key_name(request.headers.get('X-API-Key')),
        'status': 'waiting',
        'task_type': 'get_live_video',
        'url': url,
        'start': start,
        'duration': duration,
        'video_format': video_format,
        'audio_format': audio_format
    }
    save_tasks(tasks)

    return jsonify({'status': 'waiting', 'task_id': task_id})

@app.route('/get_live_audio', methods=['POST'])
@auth.check_api_key('get_live_audio')
def get_live_audio():
    data = request.json
    url = data.get('url')
    start = data.get('start', 0)
    duration = data.get('duration', 5)
    audio_format = data.get('audio_format', 'bestaudio')
    
    if not url:
        return jsonify({'status': 'error', 'message': 'URL is required'}), 400
    
    task_id = generate_random_id()
    # keys = load_keys()
    # key_name = auth.get_key_name(request.headers.get('X-API-Key'))
    # key_info = keys[key_name]

    # if 'task_ids' not in key_info:
    #     key_info['task_ids'] = []
    # key_info['task_ids'].append(task_id)
    # keys[key_name] = key_info
    # auth.save_keys(keys)

    tasks = load_tasks()
    tasks[task_id] = {
        'key_name': auth.get_key_name(request.headers.get('X-API-Key')),
        'status': 'waiting',
        'task_type': 'get_live_audio',
        'url': url,
        'start': start,
        'duration': duration,
        'video_format': 'bestvideo',
        'audio_format': audio_format
    }
    save_tasks(tasks)

    return jsonify({'status': 'waiting', 'task_id': task_id})

@app.route('/status/<task_id>', methods=['GET'])
def status(task_id):
    tasks = load_tasks()
    if task_id not in tasks:
        return jsonify({'status': 'error', 'message': 'Task ID not found'}), 404
    return jsonify(tasks[task_id])

@app.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    file_path = os.path.abspath(os.path.join(DOWNLOAD_DIR, filename))

    if not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404
    if not file_path.startswith(os.path.abspath(DOWNLOAD_DIR)):
        return jsonify({"error": "Access denied"}), 403
    
    if filename.endswith('info.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        params = request.args
        
        if params:
            filtered_data = {}
            for key, value in params.items():
                if key in data:
                    filtered_data[key] = data[key]
                elif key == 'qualities':
                    qualities = {"audio": {}, "video": {}}
                    for f in data['formats']:
                        if f.get('format_note') in ['unknown', 'storyboard']: continue
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('abr'):
                            qualities["audio"][f['format_id']] = {
                                "abr": int(f['abr']),
                                "acodec": f['acodec'],
                                "audio_channels": int(f.get('audio_channels', 0)),
                                "filesize": int(f.get('filesize') or f.get('filesize_approx') or 0)
                            }
                        elif f.get('acodec') == 'none' and f.get('vcodec') != 'none' and f.get('height') and f.get('fps') :
                            video_size = int(f.get('filesize') or f.get('filesize_approx') or 0)
                            qualities["video"][f['format_id']] = {
                                "height": int(f['height']),
                                "width": int(f['width']),
                                "fps": int(f['fps']),
                                "vcodec": f['vcodec'],
                                "format_note": f.get('format_note', 'unknown'),
                                "dynamic_range": f.get('dynamic_range', 'unknown'),
                                "filesize": video_size
                            }
                    qualities["video"] = dict(sorted(qualities["video"].items(), key=lambda x: (x[1]['height'], x[1]['fps'])))
                    qualities["audio"] = dict(sorted(qualities["audio"].items(), key=lambda x: x[1]['abr']))
                    filtered_data[key] = qualities
            if filtered_data:
                return jsonify(filtered_data)
            else:
                return jsonify({"error": "No matching parameters found"}), 404
        return jsonify(data)
    return send_from_directory(DOWNLOAD_DIR, filename)

@app.route('/create_key', methods=['POST'])
@auth.check_api_key('create_key')
def create_key():
    data = request.json
    name = data.get('name')
    permissions = data.get('permissions')
    if not name or not permissions:
        return jsonify({'error': 'Name and permissions are required'}), 400
    new_key = auth.create_api_key(name, permissions)
    return jsonify({'message': 'API key created successfully', 'name': name, 'key': new_key}), 201

@app.route('/delete_key/<name>', methods=['DELETE'])
@auth.check_api_key('delete_key')
def delete_key(name):
    if auth.delete_api_key(name):
        return jsonify({'message': 'API key deleted successfully', 'name': name}), 200
    return jsonify({'error': 'The key name does not exist'}), 403

@app.route('/get_key/<name>', methods=['GET'])
@auth.check_api_key('get_key')
def get_key(name):
    keys = load_keys()
    if name in keys:
        return jsonify({'message': 'API key get successfully', 'name': name, 'key': keys[name]['key']}), 200
    return jsonify({'error': 'The key name does not exist'}), 403

@app.route('/get_keys', methods=['GET'])
@auth.check_api_key('get_keys')
def get_keys():
    keys = load_keys()
    return jsonify(keys), 200

@app.route('/get_cookies', methods=['GET'])
@auth.check_api_key('get_cookies')
def get_cookies():
    try:

      # import sqlite3, json, base64, hashlib
      # from Crypto.Cipher import AES

        # Пути к профилю Chrome (папка Default) и Local State
        chrome_profile = "/chrome-data/.config/google-chrome/Default"
        cookies_db_path = f"{chrome_profile}/Cookies"
        local_state_path = "/chrome-data/.config/google-chrome/Local State"

        # Читаем ключ шифрования из Local State, если он там есть (Chrome 80+ Windows)
        def get_encryption_key_from_local_state():
            try:
                with open(local_state_path, "r") as ls_file:
                    local_state = json.load(ls_file)
                # Извлекаем и декодируем значение os_crypt.encrypted_key
                encrypted_key_b64 = local_state.get("os_crypt", {}).get("encrypted_key")
                if not encrypted_key_b64:
                    return None
                encrypted_key = base64.b64decode(encrypted_key_b64)  # DPAPI encrypted key (Windows)
                # На Windows ключ зашифрован DPAPI и содержит префикс "DPAPI"
                if encrypted_key.startswith(b"DPAPI"):
                    encrypted_key = encrypted_key[5:]  # убираем строку "DPAPI"
                # Попытка расшифровать с использованием CryptUnprotectData (только Windows)
                try:
                    import ctypes, ctypes.wintypes
                    CryptUnprotectData = ctypes.windll.crypt32.CryptUnprotectData
                    class DATA_BLOB(ctypes.Structure):
                        _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
                    blob_in = DATA_BLOB(len(encrypted_key), ctypes.create_string_buffer(encrypted_key))
                    blob_out = DATA_BLOB()
                    if CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
                        # Считываем расшифрованные байты ключа
                        ptr = ctypes.cast(blob_out.pbData, ctypes.c_void_p)
                        key_bytes = ctypes.string_at(ptr.value, blob_out.cbData)
                        return key_bytes
                except Exception:
                    return None
            except Exception:
                pass
            return None

        # Функция расшифровки значения cookie
        def decrypt_cookie(encrypted_value, key=None):
            """Decrypts an encrypted cookie value (bytes) using the provided key or derived static key."""
            # Если задан ключ (для Windows scenario), иначе получаем через PBKDF2 с "peanuts"
            if key is None:
                # Статический пароль и соль для Linux fallback
                password = b"peanuts"
                salt = b"saltysalt"
                # Длина ключа по умолчанию 16 (AES-128)
                key_length = 16
                # Определяем режим по формату encrypted_value
                if encrypted_value[:3] in (b"v10", b"v11"):
                    blob = encrypted_value
                    # Если длина (без префикса 3 байта) не кратна 16, вероятно используем AES-256-GCM
                    if (len(blob) - 3) % 16 != 0:
                        key_length = 32  # 256-битный ключ для AES-256
                # Генерируем ключ PBKDF2-HMAC-SHA1
                key = hashlib.pbkdf2_hmac("sha1", password, salt, 1, dklen=key_length)
            # Расшифровываем в зависимости от формата префикса
            if encrypted_value[:3] in (b"v10", b"v11"):
                blob = encrypted_value
                # AES-256-GCM формат: [ префикс3 | 12байт nonce | ciphertext+tag ]
                if (len(blob) - 3) % 16 != 0:
                    nonce = blob[3:15]
                    ciphertext = blob[15:-16]
                    tag = blob[-16:]
                    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                    plaintext = cipher.decrypt(ciphertext)
                    try:
                        cipher.verify(tag)  # проверяем целостность
                    except ValueError:
                        raise Exception("Failed to verify GCM tag – wrong key or corrupted data")
                    decrypted = plaintext
                else:
                    # AES-128-CBC формат: [префикс3 | ciphertext (IV фиксированный) ]
                    iv = b" " * 16  # IV из 16 пробелов
                    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                    ciphertext = blob[3:]
                    plaintext = cipher.decrypt(ciphertext)
                    # Удаляем PKCS#5 padding
                    pad_len = plaintext[-1]
                    decrypted = plaintext[:-pad_len]
                    # Удаляем префикс SHA256 домена (32 байта), если он присутствует
                    if len(decrypted) >= 32:
                        decrypted = decrypted[32:]
                return decrypted.decode("utf-8", errors="ignore")
            else:
                # Если префикса нет (возможный нешифрованный сценарий или иной формат)
                return encrypted_value.decode("utf-8", errors="ignore")

        # Открываем соединение с базой cookies
        conn = sqlite3.connect(cookies_db_path)
        cursor = conn.cursor()
        # Фильтруем по домену youtube.com (включая субдомены)
        cursor.execute("""
            SELECT host_key, path, is_secure, expires_utc, name, value, encrypted_value, has_expires 
            FROM cookies 
            WHERE host_key = 'youtube.com' OR host_key LIKE '%.youtube.com'
        """)
        rows = cursor.fetchall()
        conn.close()

        # Попытка получить мастер-ключ (для Windows; на Linux обычно None)
        master_key = get_encryption_key_from_local_state()

        # Подготавливаем файл для вывода cookies
        output_lines = []
        output_lines.append("# Netscape HTTP Cookie File")
        output_lines.append(f"# This file was generated by a script on Chrome profile: {chrome_profile}")
        for host_key, path, is_secure, expires_utc, name, value, enc_value, has_expires in rows:
            # Определяем актуальное значение cookie (раскодированное)
            if enc_value not in (None, b""):
                try:
                    # sqlite3 может вернуть BLOB как memoryview – преобразуем в bytes
                    if not isinstance(enc_value, (bytes, bytearray)):
                        enc_bytes = bytes(enc_value)
                    else:
                        enc_bytes = enc_value
                    cookie_val = decrypt_cookie(enc_bytes, key=master_key)
                except Exception as e:
                    cookie_val = ""  # не удалось расшифровать
            else:
                cookie_val = value or ""
            # Определяем флаг субдоменов и формат домена в файле
            include_subdomains = "FALSE"
            domain_out = host_key
            if host_key.startswith("."):
                include_subdomains = "TRUE"
            # Если домен без точки, оставляем include_subdomains FALSE (cookie для точного хоста)
            # Формируем флаг secure
            secure_flag = "TRUE" if is_secure else "FALSE"
            # Время истечения (UTC). Преобразуем из формата Chrome (микросекунды с 1601) в Unix time
            if has_expires and expires_utc:
                # Chrome stores timestamps as microseconds since 1601-01-01
                expires_unix = (expires_utc - 11644473600000000) // 1000000
            else:
                expires_unix = 0  # сессионный cookie
            # Собираем строку cookie
            line = f"{domain_out}\t{include_subdomains}\t{path}\t{secure_flag}\t{expires_unix}\t{name}\t{cookie_val}"
            output_lines.append(line)
            #print(line)

        # Запись в файл cookies.txt
        with open("/app/youtube_cookies.txt", "w") as f:
            f.write("\n".join(output_lines))

#        return f"\n".join(output_lines), 200
        return 'ok', 200
    except Exception as e:
        return f"Error exporting cookies: {e}", 500

@app.route('/check_permissions', methods=['POST'])
def check_permissions():
    data = request.json
    permissions = data.get('permissions')

    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return jsonify({'error': 'No API key provided'}), 401
    key_info = auth.get_key_info(api_key)
    if not key_info:
        return jsonify({'error': 'Invalid API key'}), 401
    current_permissions = key_info['permissions']

    if set(permissions).issubset(current_permissions):
        return jsonify({'message': 'Permissions granted'}), 200
    return jsonify({'message': 'Insufficient permissions'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0')
