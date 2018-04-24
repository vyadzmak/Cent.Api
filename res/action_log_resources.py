from models.db_models.models import ActionLog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort,reqparse

action_log_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'code':fields.Integer
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
            action_log.code = json_data['code']
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
            action_log= ActionLog(message=json_data["message"])
            session.add(action_log)
            session.commit()
            return action_log, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Action Log")