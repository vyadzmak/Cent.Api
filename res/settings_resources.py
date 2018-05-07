from models.db_models.models import Settings
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

settings_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'value': fields.String

}

parser = reqparse.RequestParser()


class SettingsResource(Resource):
    @marshal_with(settings_fields)
    def get(self, id):
        setting = session.query(Settings).filter(Settings.id == id).first()
        if not setting:
            abort(404, message=" Settings {} doesn't exist".format(id))
        return setting

    def delete(self, id):
        try:
            setting = session.query(Settings).filter(Settings.id == id).first()
            if not setting:
                abort(404, message=" Settings {} doesn't exist".format(id))
            session.delete(setting)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove  Settings")

    @marshal_with(settings_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            setting_setting = session.query(Settings).filter(Settings.id == id).first()
            setting_setting.name= json_data['name']
            setting_setting.value = json_data['value']
            session.add(setting_setting)
            session.commit()
            return setting_setting, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update  Settings")


class SettingsListResource(Resource):
    @marshal_with(settings_fields)
    def get(self):
        settings = session.query(Settings).all()
        return settings

    @marshal_with(settings_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)

            setting = Settings(name=json_data["name"], value=json_data["value"])
            session.add(setting)
            session.commit()
            return setting, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record  Settings")
