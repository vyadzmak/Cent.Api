from models.db_models.models import ActionLog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

user_login_fields = {
    # 'id': fields.Integer,
    'login': fields.String,
    # 'password': fields.String,
    # 'token': fields.String,
    # 'user_id': fields.Integer,
    # 'registration_date': fields.DateTime,
    # 'last_login_date': fields.DateTime,
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

user_data = {
    'id': fields.Integer(attribute="id"),
    'first_name': fields.String(attribute="first_name"),
    'last_name': fields.String(attribute="last_name"),
    # 'lock_state': fields.Boolean,
    # 'client_id': fields.Integer,
    # 'client': fields.Nested(client_fields),
    # 'user_role_id': fields.Integer,
    # 'user_role': fields.Nested(user_role_fields),
    'login_data': fields.Nested(user_login_fields)
}

action_log_types = {
    'id': fields.Integer,
    'message': fields.String,
    'code': fields.Integer
}

action_log_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'user_id': fields.Integer,
    'action_log_type': fields.Nested(action_log_types),
    'user_data': fields.Nested(user_data)
}

parser = reqparse.RequestParser()


class ActionLogResource(Resource):
    @marshal_with(action_log_fields)
    def get(self, id):
        action_log = session.query(ActionLog).filter(ActionLog.id == id).first()
        if not action_log:
            abort(404, message="Action log {} doesn't exist".format(id))
        return action_log

    def delete(self, id):
        try:
            action_log = session.query(ActionLog).filter(ActionLog.id == id).first()
            if not action_log:
                abort(404, message="Action log {} doesn't exist".format(id))
            session.delete(action_log)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Action Type")

    @marshal_with(action_log_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            action_log = session.query(ActionLog).filter(ActionLog.id == id).first()
            action_log.message = json_data['message']
            action_log.action_type_id = json_data['action_type_id']
            action_log.user_id = json_data['user_id']
            session.add(action_log)
            session.commit()
            return action_log, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Action Log")


class ActionLogListResource(Resource):
    @marshal_with(action_log_fields)
    def get(self):
        action_log = session.query(ActionLog).all()
        return action_log

    @marshal_with(action_log_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            action_log = ActionLog(message=json_data["message"], user_id=json_data["user_id"],
                                   action_type_id=json_data["action_type_id"])
            session.add(action_log)
            session.commit()
            return action_log, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Action Log")
