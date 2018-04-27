from models.db_models.models import GroupObjectRights
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

group_object_rights_fields = {
    'id': fields.Integer,
    'group_id':fields.Integer,
    'object_id':fields.Integer,
    'data':fields.String,
    'user_creator_id':fields.Integer
}

parser = reqparse.RequestParser()


class GroupObjectRightsResource(Resource):
    @marshal_with(group_object_rights_fields)
    def get(self, id):
        group_object_right = session.query(GroupObjectRights).filter(GroupObjectRights.id == id).first()
        if not group_object_right:
            abort(404, message="Group Object Rights  {} doesn't exist".format(id))
        return group_object_right

    def delete(self, id):
        try:
            group_object_right = session.query(GroupObjectRights).filter(GroupObjectRights.id == id).first()
            if not group_object_right:
                abort(404, message="Group Object Rights  {} doesn't exist".format(id))
            session.delete(group_object_right)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Group Object Rights ")

    @marshal_with(group_object_rights_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            group_object_right = session.query(GroupObjectRights).filter(GroupObjectRights.id == id).first()
            group_object_right.data = json_data['data']
            session.add(group_object_right)
            session.commit()
            return group_object_right, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Group Object Rights")


class GroupObjectRightsListResource(Resource):
    @marshal_with(group_object_rights_fields)
    def get(self):
        group_object_rights = session.query(GroupObjectRights).all()
        return group_object_rights

    @marshal_with(group_object_rights_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # group_id, user_creator_id, object_id, data=None
            data = None
            if ('data' in json_data) == True:
                data = json_data['data']
            group_object_right = GroupObjectRights(group_id=json_data["group_id"],
                                                   user_creator_id=json_data["user_creator_id"],
                                                   object_id=json_data["object_id"],
                                                   data=data)
            session.add(group_object_right)
            session.commit()
            return group_object_right, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Group Object Rights")
