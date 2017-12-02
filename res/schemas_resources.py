from models.db_models.models import Schemas
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_converters.schema_data_converter as s_d_converter
import models.app_models.schema_models.schema_model as s_model
import datetime
from sqlalchemy import and_
import copy

import modules.db_converters.field_items_converter as items_converter
schema_type_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'title': fields.String()
}

schema_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,
    'group_title': fields.String,
    'description': fields.String,
    'schema_type_id': fields.Integer,
    'client_id': fields.Integer,
    'user_id': fields.Integer,
    'creation_date': fields.DateTime,
    'update_date': fields.DateTime,
    'data': fields.String,
    'is_show': fields.Boolean
}


class SchemaCatalogsListResource(Resource):
    @marshal_with(schema_fields)
    def get(self, clientId):
        schemas = session.query(Schemas).filter(
            and_(Schemas.schema_type_id == 3,
                 Schemas.client_id == clientId)
        ).all()
        if not schemas:
            abort(404, message="Schemas not found")
        return schemas


class SchemaLinkListResource(Resource):
    @marshal_with(schema_fields)
    def get(self, clientId):
        schemas = session.query(Schemas).filter(and_
                                                (Schemas.schema_type_id != 3),
                                                (Schemas.client_id == clientId)
                                                ).all()
        if not schemas:
            abort(404, message="Schemas not found")
        return schemas


class SchemaClientListResource(Resource):
    @marshal_with(schema_fields)
    def get(self, clientId):
        schemas = session.query(Schemas).filter(and_  (Schemas.client_id == clientId,
                                                       Schemas.is_show==True)
                                                ).all()
        if not schemas:
            abort(404, message="Schemas not found")
        return schemas


class SchemaTypesListResource(Resource):
    @marshal_with(schema_type_fields)
    def get(self):
        schema_type_list = s_model.Schema("types", "types")
        return schema_type_list.schema_types


class SchemaResource(Resource):
    @marshal_with(schema_fields)
    def get(self, id):
        schema = session.query(Schemas).filter(Schemas.id == id).first()

        if not schema:
            abort(404, message="Schema {} doesn't exist".format(id))

        result_schema = copy.deepcopy(schema)

        result_schema.data = items_converter.get_to_data_field_items(result_schema.data)


        return result_schema

    def delete(self, id):
        schema = session.query(Schemas).filter(Schemas.id == id).first()
        if not schema:
            abort(404, message="Client type {} doesn't exist".format(id))
        session.delete(schema)
        session.commit()
        return {}, 204

    @marshal_with(schema_fields)
    def put(self, id):
        json_data = request.get_json(force=True)
        schema = session.query(Schemas).filter(Schemas.id == id).first()
        schema.name = json_data['name']
        schema.title = json_data["title"],
        schema.group_title = json_data["group_title"],
        schema.description = json_data["description"],
        schema.schema_type_id = json_data["schema_type_id"],
        schema.client_id = json_data["client_id"],
        schema.user_id = json_data["user_id"]
        schema.is_show = json_data["is_show"]
        schema.update_date = datetime.datetime.now()
        schema.data = s_d_converter.convert_schema_object(json_data)
        session.add(schema)
        session.commit()
        return schema, 201


class SchemaListResource(Resource):
    @marshal_with(schema_fields)
    def get(self):
        schemas = session.query(Schemas).all()
        return schemas

    @marshal_with(schema_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)

            # name, title, group_title, description, is_catalog, data, client_id, user_id
            schema = Schemas(
                name=json_data["name"],
                title=json_data["title"],
                group_title=json_data["group_title"],
                description=json_data["description"],
                schema_type_id=json_data["schema_type_id"],
                client_id=json_data["client_id"],
                user_id=json_data["user_id"],
                is_show=json_data["is_show"]
            )
            session.add(schema)
            session.commit()
            return schema, 201
        except Exception as e:
            abort(400, message="Error while adding record Schema")
