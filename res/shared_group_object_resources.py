from models.db_models.models import SharedGroupObjects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse


shared_group_objects_fields = {
    'id': fields.Integer,
    'shared_date': fields.DateTime,
    'shared_members': fields.List(fields.Integer),
    'shared_user_id': fields.Integer,
    'lock_state':fields.Boolean,
    'object_id':fields.Integer
}

parser = reqparse.RequestParser()


class SharedGroupObjectsResource(Resource):
    @marshal_with(shared_group_objects_fields)
    def get(self, id):
        shared_group_object = session.query(SharedGroupObjects).filter(SharedGroupObjects.id == id).first()
        if not shared_group_object:
            abort(404, message="Shared Group Object {} doesn't exist".format(id))
        return shared_group_object

    def delete(self, id):
        try:
            shared_group_object = session.query(SharedGroupObjects).filter(SharedGroupObjects.id == id).first()
            if not shared_group_object:
                abort(404, message="Shared Group Object {} doesn't exist".format(id))
            session.delete(shared_group_object)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Shared Group Object")

    @marshal_with(shared_group_objects_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            shared_group_object = session.query(SharedGroupObjects).filter(SharedGroupObjects.id == id).first()
            shared_group_object.lock_state = json_data['lock_state']
            shared_group_object.group_members = json_data['group_members']
            session.add(shared_group_object)
            session.commit()
            return shared_group_object, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Shared Group Object")


class SharedGroupObjectsListResource(Resource):
    @marshal_with(shared_group_objects_fields)
    def get(self):
        shared_group_object = session.query(SharedGroupObjects).all()
        return shared_group_object

    @marshal_with(shared_group_objects_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            #shared_user_id, object_id
            shared_group_object = SharedGroupObjects(shared_user_id=json_data["shared_user_id"], object_id=json_data["object_id"])
            session.add(shared_group_object)
            session.commit()
            return shared_group_object, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Shared Group Object")
