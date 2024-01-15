from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo, ObjectId
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity, get_current_user
from datetime import datetime, timedelta
from functools import wraps
from pymongo import MongoClient

app = Flask(__name__)

# Setting up global configurations for our app
app.config['MONGODB_URI'] = 'mongodb://localhost:27017/'
app.config['SECRET_KEY'] = 'your-strong-secret-key'
app.config['JWT_SECRET_KEY'] = 'my-secret-key'
app.config["JWT_TOKEN_LOCATION"] = ["headers"] 

# Create a MongoDB client
client = MongoClient(app.config['MONGODB_URI'])
db = client.appLogin
users = db.users

jwt = JWTManager(app) 

#Create  route defult
@app.route('/') 
def index(): 
    return jsonify({"message": "Welcome to your Flask app!"})

# Create user registration route
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

   # Make sure username doesn't already exist
    existing_user = users.find_one({'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # צור משתמש חדש ב-MongoDB
    users.insert_one({'username': username, 'password': password})

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/changePassword', methods=['POST'])
def changePassword():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Check for existing user
    existing_user = users.find_one({'username': username})
    if not existing_user:
        return jsonify({'error': 'Username not found'}), 404

    # Update password (securely, using a hashing algorithm)
    users.update_one({'username': username}, {'$set': {'password': password}})

    return jsonify({'message': 'Password has been changed'}), 200


   
# Create login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # ודא שהמשתמש קיים
    user = users.find_one({'username': username})
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    if user['password'] != password:
        return jsonify({'error': 'Invalid username or password'}), 401

    # צור טוקן גישה
    access_token = create_access_token(identity=username)

    return jsonify({'access_token': access_token}), 200


# Protect a route with JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
        
     # Verify the JWT
    verified = verify_jwt()  
    if not verified:
        return jsonify({'message': 'Invalid JWT'}), 401

    # Get the user ID from the JWT
    user_id = get_jwt_identity()
    
    # Get the user claims
    claims = get_jwt_claims()

    # Return a success message
    return jsonify({'message': f'Welcome, {user_id} ({claims})'}), 200



if __name__ == '__main__':
    app.run(debug=True)