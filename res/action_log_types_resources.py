from models.db_models.models import ActionLogTypes
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort,reqparse

action_log_type_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'code':fields.Integer
}

parser = reqparse.RequestParser()

class ActionLogTypeResource(Resource):
    @marshal_with(action_log_type_fields)
    def get(self, id):
        action_log_type = session.query(ActionLogTypes).filter(ActionLogTypes.id == id).first()
        if not action_log_type:
            abort(404, message="Action log type {} doesn't exist".format(id))
        return action_log_type

    def delete(self, id):
        try:
            action_log_type = session.query(ActionLogTypes).filter(ActionLogTypes.id == id).first()
            if not action_log_type:
                abort(404, message="Action log type {} doesn't exist".format(id))
            session.delete(action_log_type)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Action Log Type")

    @marshal_with(action_log_type_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            action_log_type = session.query(ActionLogTypes).filter(ActionLogTypes.id == id).first()
            action_log_type.message = json_data['message']
            action_log_type.code = json_data['code']
            session.add(action_log_type)
            session.commit()
            return action_log_type, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Action Log Type")

class ActionLogTypeListResource(Resource):
    @marshal_with(action_log_type_fields)
    def get(self):
        action_log_types = session.query(ActionLogTypes).all()
        return action_log_types

    @marshal_with(action_log_type_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            action_log_type= ActionLogTypes(message=json_data["message"])
            session.add(action_log_type)
            session.commit()
            return action_log_type, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Action Log Type")