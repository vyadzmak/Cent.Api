from models.db_models.models import UserRouteAccess
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

user_route_access_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'data':fields.String,
}

parser = reqparse.RequestParser()


class UserRouteAccessResource(Resource):
    @marshal_with(user_route_access_fields)
    def get(self, id):
        user_route_access = session.query(UserRouteAccess).filter(UserRouteAccess.id == id).first()
        if not user_route_access:
            abort(404, message="User Route Access  {} doesn't exist".format(id))
        return user_route_access

    def delete(self, id):
        try:
            user_route_access = session.query(UserRouteAccess).filter(UserRouteAccess.id == id).first()
            if not user_route_access:
                abort(404, message="User Route Access  {} doesn't exist".format(id))
            session.delete(user_route_access)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove User Route Access")

    @marshal_with(user_route_access_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            user_route_access = session.query(UserRouteAccess).filter(UserRouteAccess.id == id).first()
            user_route_access.data = json_data['data']
            session.add(user_route_access)
            session.commit()
            return user_route_access, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update User Route Access")


class UserRouteAccessListResource(Resource):
    @marshal_with(user_route_access_fields)
    def get(self):
        user_route_access = session.query(UserRouteAccess).all()
        return user_route_access

    @marshal_with(user_route_access_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # group_id, user_creator_id, object_id, data=None
            data = None
            if ('data' in json_data) == True:
                data = json_data['data']
            user_route_access = UserRouteAccess(user_id=json_data["user_id"],
                                                   data=data)
            session.add(user_route_access)
            session.commit()
            return user_route_access, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record User Route Access")
