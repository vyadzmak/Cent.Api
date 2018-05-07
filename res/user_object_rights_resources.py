from models.db_models.models import UserObjectRights
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

user_object_rights_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'object_id':fields.Integer,
    'data':fields.String,
    'user_creator_id':fields.Integer
}

parser = reqparse.RequestParser()


class UserObjectRightsResource(Resource):
    @marshal_with(user_object_rights_fields)
    def get(self, id):
        user_object_right = session.query(UserObjectRights).filter(UserObjectRights.id == id).first()
        if not user_object_right:
            abort(404, message="User Object Rights  {} doesn't exist".format(id))
        return user_object_right

    def delete(self, id):
        try:
            user_object_right = session.query(UserObjectRights).filter(UserObjectRights.id == id).first()
            if not user_object_right:
                abort(404, message="User Object Rights  {} doesn't exist".format(id))
            session.delete(user_object_right)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove User Object Rights ")

    @marshal_with(user_object_rights_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            user_object_right = session.query(UserObjectRights).filter(UserObjectRights.id == id).first()
            user_object_right.data = json_data['data']
            session.add(user_object_right)
            session.commit()
            return user_object_right, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update User Object Rights")


class UserObjectRightsListResource(Resource):
    @marshal_with(user_object_rights_fields)
    def get(self):
        user_object_rights = session.query(UserObjectRights).all()
        return user_object_rights

    @marshal_with(user_object_rights_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # group_id, user_creator_id, object_id, data=None
            data = None
            if ('data' in json_data) == True:
                data = json_data['data']
            user_object_right = UserObjectRights(user_id=json_data["user_id"],
                                                   user_creator_id=json_data["user_creator_id"],
                                                   object_id=json_data["object_id"],
                                                   data=data)
            session.add(user_object_right)
            session.commit()
            return user_object_right, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record User Object Rights")
