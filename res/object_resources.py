from models.db_models.models import Objects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_converters.schema_data_converter as s_d_converter
import models.app_models.schema_models.schema_model as s_model
import datetime
import modules.dynamic_table_generator.dynamic_table_objects_generator as dt_generator
from sqlalchemy import and_

schema_type_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'title': fields.String()
}

object_fields = {
    'id': fields.Integer,
    'schema_id': fields.Integer,
    'client_id': fields.Integer,
    'user_id': fields.Integer,
    'creation_date': fields.DateTime,
    'update_date': fields.DateTime,
    'data': fields.String
}



class ObjectSchemaListResource(Resource):
    #@marshal_with(object_fields)
    def get(self,schemaId):
        objects =  session.query(Objects).filter(Objects.schema_id == schemaId).all()

        result = dt_generator.generate_dynamic_table_by_objects(objects)

        return result



class ObjectResource(Resource):
    @marshal_with(object_fields)
    def get(self, id):
        object = session.query(Objects).filter(Objects.id == id).first()
        if not object:
            abort(404, message="Object {} doesn't exist".format(id))
        return object

    def delete(self, id):
        object = session.query(Objects).filter(Objects.id == id).first()
        if not object:
            abort(404, message="Object {} doesn't exist".format(id))
        session.delete(object)
        session.commit()
        return {}, 204

    @marshal_with(object_fields)
    def put(self, id):
        json_data = request.get_json(force=True)
        object = session.query(Objects).filter(Objects.id == id).first()
        object.schema_id = json_data["schema_id"],
        object.client_id = json_data["client_id"],
        object.user_id = json_data["user_id"]
        object.update_date = datetime.datetime.now()
        #object.data = s_d_converter.convert_schema_object(json_data)
        session.add(object)
        session.commit()
        return object, 201


class ObjectListResource(Resource):
    @marshal_with(object_fields)
    def get(self):
        objects = session.query(Objects).all()
        return objects

    @marshal_with(object_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            object = Objects(
                schema_id=json_data["schema_id"],
                client_id=json_data["client_id"],
                user_id=json_data["user_id"],
                parent_id=json_data["parent_id"],
                fields = json_data["fields"]
            )
            session.add(object)
            session.commit()
            return object, 201
        except Exception as e:
            abort(400, message="Error while adding record Schema")
