from models.db_models.models import ObjectSettings
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

object_settings_fields = {
    'id': fields.Integer,
    'object_id': fields.Integer,
    'data': fields.String,
}

parser = reqparse.RequestParser()


class ObjectSettingsResource(Resource):
    @marshal_with(object_settings_fields)
    def get(self, id):
        object_setting = session.query(ObjectSettings).filter(ObjectSettings.id == id).first()
        if not object_setting:
            abort(404, message="Object Settings {} doesn't exist".format(id))
        return object_setting

    def delete(self, id):
        try:
            object_setting = session.query(ObjectSettings).filter(ObjectSettings.id == id).first()
            if not object_setting:
                abort(404, message="Object Settings {} doesn't exist".format(id))
            session.delete(object_setting)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Object Settings")

    @marshal_with(object_settings_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            object_setting = session.query(ObjectSettings).filter(ObjectSettings.id == id).first()
            object_setting.data = json_data['data']
            session.add(object_setting)
            session.commit()
            return object_setting, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Object Settings")


class ObjectSettingsListResource(Resource):
    @marshal_with(object_settings_fields)
    def get(self):
        object_settings = session.query(ObjectSettings).all()
        return object_settings

    @marshal_with(object_settings_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            data = None
            if ('data' in json_data) == True:
                data = json_data['data']
            object_setting = ObjectSettings(object_id=json_data["object_id"], data=data)
            session.add(object_setting)
            session.commit()
            return object_setting, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Object Settings")
