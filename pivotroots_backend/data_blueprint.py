import os
import random
import string
import base64
import datetime
from database import DB
from flask import current_app
from flask import Blueprint, request, jsonify

data = Blueprint("data_blueprint",__name__)
print("data_blueprint executed")

db = DB()

import jwt
from datetime import datetime, timedelta
from functools import wraps

UPLOAD_FOLDER = "uploads"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers
        bearer_token = auth_header.get('Authorization')

        if ( not bearer_token or (not bearer_token.startswith("Bearer"))):
            return jsonify({'message' : 'Bearer is missing'}), 401

        token = bearer_token.split()[1]

        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            decoded_token = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])

            check_user = db.query_db("SELECT user_id, username, email, user_type FROM users WHERE user_id=%s", (decoded_token["user_id"],))
            user_info = check_user[0]

        except Exception as err:
            print("ERR", err)
            return jsonify({'message' : 'Token is invalid !!'}), 401

        return  f(user_info, *args, **kwargs)
    return decorated

@data.route("/user-page", methods=['GET'])
@token_required
def user_page(user_info):

    print("USerinfo", user_info)

    if user_info["user_type"] == "admin":
        get_all_users = db.query_db("SELECT * FROM users WHERE user_type != 'admin'")
        print("ALL USER GROUP DATA", get_all_users)

        return jsonify({'message' : 'users fetched successfully', 'status':'success', 'data': {'users': get_all_users}}), 200
        

    elif user_info["user_type"] == "user":
        get_all_files = db.query_db("SELECT file_id,file_name,file_path,file_type,created_at FROM upload_data WHERE file_owner=%s ORDER BY created_at DESC", (user_info['user_id'],))
        return jsonify({'message' : 'user data fetched successfully', 'status':'success', 'data': {'userdata': get_all_files}}), 200

    else:
        return jsonify({'message' : 'User Type invalid', 'status':'failure'}), 401

@data.route("/documents/<folder>/<filename>", methods=['GET','POST'])
@token_required
def document_upload(user_info, folder, filename):
    if request.method == 'GET':

        revision = request.args.get('revision')

        file_path = os.path.join(UPLOAD_FOLDER, folder, filename)

        get_all_files = db.query_db("SELECT * FROM upload_data WHERE file_owner=%s AND file_path=%s ORDER BY created_at DESC", (user_info['user_id'], file_path,))
        if not get_all_files:
            return jsonify({'message' : 'File does not exist for this user', 'status':'failure'}), 401

        try:
            is_convertable = int(revision)
        except Exception as err:
            return jsonify({'message' : 'revision type should be a number', 'status':'failure'}), 401

        if int(revision) > len(get_all_files):
            return jsonify({'message' : 'revision does not exist', 'status':'failure'}), 401

        if revision:
            load_file = get_all_files[int(revision)]
        else:
            load_file = get_all_files[0]
            

        file_text = open(load_file["file_path_uploads"],'rb')
        file_read = file_text.read()
        encoded_data = base64.b64encode(file_read).decode('ascii')

        data_info = {
            "file_name": load_file["file_name"]
        }

        return jsonify({'message' : 'File fetched successfully', 'status':'success', 'data': {'user_id': user_info["user_id"], "encoded_data": encoded_data, "data_info": data_info }}), 200

    elif request.method == 'POST':

        uploaded_file = request.files
        file = uploaded_file["file"]
        file_type = file.content_type
        secure_filename = file.filename

        file_ext = secure_filename.split(".")[1]
        url_file_ext = filename.split(".")[1]

        if file_ext != url_file_ext:
            return jsonify({'message' : 'File extension doesnt match url filename extension', 'status':'failure'}), 401
        
        path_exists = os.path.exists(os.path.join(UPLOAD_FOLDER, folder))
        if not path_exists:
            os.mkdir(os.path.join(UPLOAD_FOLDER, folder))

        file_name = f'{filename.split(".")[0]}.{file_ext}'

        random_gen = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        file_save_path = os.path.join(UPLOAD_FOLDER, folder, file_name)
        file_uploads_path = os.path.join(UPLOAD_FOLDER, folder, f"{random_gen}.{file_ext}")
        
        file.save(file_uploads_path)

        added_file = db.run("INSERT INTO upload_data (file_id, file_name, file_path, file_owner, file_type, file_path_uploads) VALUES (gen_random_uuid(),%s,%s,%s,%s,%s)", (file_name, file_save_path, user_info["user_id"], file_type, file_uploads_path, ))

        if not added_file:
            return jsonify({'message' : 'Unable to add file', 'status':'failure'}), 401

        return jsonify({'message' : 'File added successfully', 'status':'success', 'data': {'user_id': user_info["user_id"]}}), 201
