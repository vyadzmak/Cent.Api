from models.db_models.models import ObjectViews
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

object_views_fields = {
    'id': fields.Integer,
    'object_id': fields.Integer,
    'user_creator_id': fields.Integer,
    'data': fields.String,
}

parser = reqparse.RequestParser()


class ObjectViewsResource(Resource):
    @marshal_with(object_views_fields)
    def get(self, id):
        object_view = session.query(ObjectViews).filter(ObjectViews.id == id).first()
        if not object_view:
            abort(404, message="Object Views {} doesn't exist".format(id))
        return object_view

    def delete(self, id):
        try:
            object_view = session.query(ObjectViews).filter(ObjectViews.id == id).first()
            if not object_view:
                abort(404, message="Object Views {} doesn't exist".format(id))
            session.delete(object_view)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Object Views")

    @marshal_with(object_views_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            object_view = session.query(ObjectViews).filter(ObjectViews.id == id).first()
            object_view.data = json_data['data']
            session.add(object_view)
            session.commit()
            return object_view, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Object Views")


class ObjectViewsListResource(Resource):
    @marshal_with(object_views_fields)
    def get(self):
        object_views = session.query(ObjectViews).all()
        return object_views

    @marshal_with(object_views_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            data = None
            if ('data' in json_data) == True:
                data = json_data['data']
            object_view = ObjectViews(object_id=json_data["object_id"],user_creator_id=json_data["user_creator_id"], data=data)
            session.add(object_view)
            session.commit()
            return object_view, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Object Views")
