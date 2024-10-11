#!/usr/bin/env python3

from flask import request, session, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        # session['page_views'] = None
        # session['user_id'] = None
        session.clear()

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return (user.to_dict()), 200
        return {}, 204
class Login(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = json_data.get('username')
        password = json_data.get('password')
        
        user = User.query.filter(User.username == username).first()
        if user.authenticate(password):
            session['user_id'] = user.id  # Set session user_id
            return (user.to_dict()), 200

        return jsonify({'error': 'Invalid credentials'}), 401

class Logout(Resource):
    def delete(self):
        session.clear()
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
  