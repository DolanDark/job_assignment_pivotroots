from database import DB
import jwt
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask import current_app

autho = Blueprint("autho", __name__)
autho.secret_key = 'secretval'
print("autho_blueprint executed")

bcrypt = Bcrypt() 
db = DB()

@autho.route("/", methods=["GET","POST"])
@autho.route("/login", methods=["GET","POST"])
def login():

    if request.method == 'GET':
        return jsonify({'message' : 'Invalid method', 'status':'failure'}), 405

    elif request.method == 'POST':

        try:
            request_json = request.get_json(force=True)
        except Exception as err:
            print("Error Invalid Json")
            return jsonify({'message' : 'Invalid Json', 'status':'failure'}), 401

        email = request_json.get("email")
        password = request_json.get("password")

        user_query = db.query_db("SELECT * FROM users WHERE email=%s", (email,))

        if not user_query:
            return jsonify({'message' : 'User with email doesnt exist', 'status':'failure'}), 401

        user_exists = user_query[0]

        is_password_valid = bcrypt.check_password_hash(user_exists["password"], password)

        # return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

        if is_password_valid:

            del user_exists['password']
            del user_exists['created_at']
            del user_exists['id']

            jwt_token = jwt.encode(user_exists, current_app.secret_key)

            return jsonify({'message' : 'User logged in successfully', 'status':'success', 'data': {'token': jwt_token}}), 200
        else:
            return jsonify({'message' : 'Invalid password', 'status':'failure'}), 403

    else:
        return jsonify({'message' : 'Invalid method'}), 401
        

# return redirect(url_for('data_blueprint.user_page'))
# @autho.route("/info", methods=["GET","POST"])
#     return render_template("info.html")

@autho.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

        try:
            request_json = request.get_json(force=True)
        except Exception as err:
            print("Error Invalid Json")
            return jsonify({'message' : 'Invalid Json', 'status':'failure'}), 401

        username = request_json.get("username")
        email = request_json.get("email")
        password = request_json.get("password")

        if not(username or password or password):
            return jsonify({'message' : 'missing necessary params', 'status':'failure'}), 401

        get_user = db.execute("SELECT 1 FROM users WHERE email=%s", (email,))

        if (get_user):
            return jsonify({'message' : 'email already exists', 'status':'failure'}), 401

        hashed_password = bcrypt.generate_password_hash (password).decode('utf-8') 

        new_user = db.run("INSERT INTO users (user_id, username, password, email, user_type) VALUES (gen_random_uuid(),%s,%s,%s,%s)", (username, hashed_password, email, "user"))
        
        if not new_user:
            return jsonify({'message' : 'Query Failed', 'status':'failure'}), 401

        created_user = db.execute("SELECT user_id FROM users WHERE email=%s", (email,))

        return jsonify({'message' : 'user successfully created', 'status':'success', 'data':{'user_id': created_user[0]}}), 200
    else:
        return jsonify({'message' : 'Invalid method', 'status':'failure'}), 405

@autho.route('/logout')
def logout():
    # session.pop('user')
    # return redirect(url_for('autho.login'))
    print("logout")
