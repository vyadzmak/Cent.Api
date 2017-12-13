from models.db_models.models import Users, UserLogins
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import copy
import base64
user_login_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'token': fields.String,
    'user_id': fields.Integer,
    'registration_date': fields.DateTime,
    'last_login_date': fields.DateTime,
}

client_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'registration_date': fields.DateTime(attribute="registration_date"),
    'registration_number': fields.String(attribute="registration_number")

}

user_role_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'lock_state': fields.Boolean,
    'client_id': fields.Integer,
    'client': fields.Nested(client_fields),
    'user_role_id': fields.Integer,
    'user_role': fields.Nested(user_role_fields),
    'login_data': fields.Nested(user_login_fields)
}


class ClientUsersListResource(Resource):
    @marshal_with(user_fields)
    def get(self,id):
        users = session.query(Users).filter(Users.client_id==id).all()
        return users

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(Users).filter(Users.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user

    def delete(self, id):
        try:
            client = session.query(Users).filter(Users.id == id).first()
            if not client:
                abort(404, message="User {} doesn't exist".format(id))
            session.delete(client)
            session.commit()
            return {}, 204

        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove user")

    @marshal_with(user_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            user = session.query(Users).filter(Users.id == id).first()
            user.first_name = json_data['name']
            user.last_name = json_data["registration_number"]
            user.lock_state = json_data["lock_state"]
            user.client_id = json_data["client_id"]
            user.user_role_id = json_data["user_role_id"]
            session.add(user)
            session.commit()
            return user, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update user")


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = session.query(Users).all()
        return users

    @marshal_with(user_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            user = Users(first_name=json_data["first_name"], last_name=json_data["last_name"],
                         lock_state=json_data["lock_state"], client_id=json_data["client_id"],
                         user_role_id=json_data["user_role_id"])
            session.add(user)
            l = json_data["login_data"][0]
            session.commit()
            user_id = user.id
            log =l["login"]
            passw =l["password"]

            o_password = copy.copy(passw)
            t = bytes(passw, 'utf-8')
            o_password = str(base64.b64encode(t))
            login = UserLogins(log,o_password,user_id)
            session.add(login)
            session.commit()
            return user, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record User")

class TestResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)
        vals =parser.parse_args()
        id = vals["id"]
        name = vals["name"]
        return 0