from models.db_models.models import UserGroups
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
    'user_group_user_data':fields.Nested(user_group_user_data),
    'lock_state':fields.Boolean,
    'created_date':fields.DateTime,
    'group_members':fields.List(fields.Integer)
}

parser = reqparse.RequestParser()


class UserGroupsResource(Resource):
    @marshal_with(user_groups_fields)
    def get(self, id):
        user_group = session.query(UserGroups).filter(UserGroups.id == id).first()
        if not user_group:
            abort(404, message="User Group  {} doesn't exist".format(id))
        return user_group

    def delete(self, id):
        try:
            user_group = session.query(UserGroups).filter(UserGroups.id == id).first()
            if not user_group:
                abort(404, message="User Group  {} doesn't exist".format(id))
            session.delete(user_group)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove User Group ")

    @marshal_with(user_groups_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            user_group = session.query(UserGroups).filter(UserGroups.id == id).first()

            user_group.user_creator_id = json_data['user_creator_id']
            user_group.group_name = json_data['group_name']
            user_group.lock_state = json_data['lock_state']
            user_group.group_members = json_data['group_members']

            session.add(user_group)
            session.commit()
            return user_group, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update User Group")


class UserGroupsListResource(Resource):
    @marshal_with(user_groups_fields)
    def get(self):
        user_groups = session.query(UserGroups).all()
        return user_groups

    @marshal_with(user_groups_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            user_group = UserGroups(user_creator_id=json_data['user_creator_id'],group_name=json_data['group_name'])
            session.add(user_group)
            session.commit()
            return user_group, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record User Group")
