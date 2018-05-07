from models.db_models.models import UserGroupSettings
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

user_login_fields = {
    'login': fields.String,
}

user_group_user_data = {
    'id': fields.Integer(attribute="id"),
    'first_name': fields.String(attribute="first_name"),
    'last_name': fields.String(attribute="last_name"),
    'login_data': fields.Nested(user_login_fields)
}

user_groups_fields = {
    'id': fields.Integer,
    'user_creator_id': fields.Integer,
    'group_name': fields.String,
    'user_group_user_data': fields.Nested(user_group_user_data),
    'lock_state': fields.Boolean,
    'created_date': fields.DateTime,
    'group_members': fields.List(fields.Integer)
}

user_group_settings = {
    'id': fields.Integer,
    'group_id': fields.Integer,
    'data': fields.String,
    'user_group_data': fields.Nested(user_groups_fields)
}

parser = reqparse.RequestParser()


class UserGroupSettingsResource(Resource):
    @marshal_with(user_group_settings)
    def get(self, id):
        user_group = session.query(UserGroupSettings).filter(UserGroupSettings.id == id).first()
        if not user_group:
            abort(404, message="User Group Settings {} doesn't exist".format(id))
        return user_group

    def delete(self, id):
        try:
            user_group = session.query(UserGroupSettings).filter(UserGroupSettings.id == id).first()
            if not user_group:
                abort(404, message="User Group Settings {} doesn't exist".format(id))
            session.delete(user_group)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove User Group Settings")

    @marshal_with(user_group_settings)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            user_group_setting = session.query(UserGroupSettings).filter(UserGroupSettings.id == id).first()
            user_group_setting.data = json_data['data']
            session.add(user_group_setting)
            session.commit()
            return user_group_setting, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update User Group Settings")


class UserGroupSettingsListResource(Resource):
    @marshal_with(user_group_settings)
    def get(self):
        user_groups = session.query(UserGroupSettings).all()
        return user_groups

    @marshal_with(user_group_settings)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            data = None
            if ('data' in json_data) == True:
                data = json_data['data']
            user_group = UserGroupSettings(group_id=json_data["group_id"], data=data)
            session.add(user_group)
            session.commit()
            return user_group, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record User Group Settings")
