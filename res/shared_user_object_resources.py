from models.db_models.models import SharedUserObjects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse


shared_user_objects_fields = {
    'id': fields.Integer,
    'shared_date': fields.DateTime,
    'shared_members': fields.List(fields.Integer),
    'shared_user_id': fields.Integer,
    'lock_state':fields.Boolean,
    'object_id':fields.Integer
}

parser = reqparse.RequestParser()


class SharedUserObjectsResource(Resource):
    @marshal_with(shared_user_objects_fields)
    def get(self, id):
        shared_user_object = session.query(SharedUserObjects).filter(SharedUserObjects.id == id).first()
        if not shared_user_object:
            abort(404, message="Shared Group Object {} doesn't exist".format(id))
        return shared_user_object

    def delete(self, id):
        try:
            shared_user_object = session.query(SharedUserObjects).filter(SharedUserObjects.id == id).first()
            if not shared_user_object:
                abort(404, message="Shared Group Object {} doesn't exist".format(id))
            session.delete(shared_user_object)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Shared Group Object")

    @marshal_with(shared_user_objects_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            shared_user_object = session.query(SharedUserObjects).filter(SharedUserObjects.id == id).first()
            shared_user_object.lock_state = json_data['lock_state']
            shared_user_object.group_members = json_data['group_members']
            session.add(shared_user_object)
            session.commit()
            return shared_user_object, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Shared Group Object")


class SharedUserObjectsListResource(Resource):
    @marshal_with(shared_user_objects_fields)
    def get(self):
        shared_user_object = session.query(SharedUserObjects).all()
        return shared_user_object

    @marshal_with(shared_user_objects_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            #shared_user_id, object_id
            shared_user_object = SharedUserObjects(shared_user_id=json_data["shared_user_id"], object_id=json_data["object_id"])
            session.add(shared_user_object)
            session.commit()
            return shared_user_object, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Shared Group Object")
