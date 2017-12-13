from models.db_models.models import Objects
from db.db import session
from flask import Flask, jsonify, request

from flask_restful import Resource, fields, marshal_with, abort, reqparse

import datetime
import modules.dynamic_table_generator.dynamic_table_objects_generator as dt_generator
from sqlalchemy import and_
import  models.app_models.object_models.object_model as object_model
import modules.json_modules.json_encoder as encoder
from sqlalchemy import and_
import modules.db_helpers.entity_helper as e_helper
import models.app_models.object_details_models.entity_details_model as e_model

class EntityResource(Resource):

    def get(self, id):

        result =e_model.EntityDetails(id)

        if result==None:
            abort(404, message="Object {} doesn't exist".format(id))
        return encoder.encode(result)

    def delete(self, id):
        try:
            object = session.query(Objects).filter(Objects.id == id).first()
            if not object:
                abort(404, message="Object {} doesn't exist".format(id))
            session.delete(object)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Entity")


    def put(self, id):
        try:

            json_data = request.get_json(force=True)
            object = session.query(Objects).filter(Objects.id == id).first()
            object.schema_id = json_data["schema_id"]
            object.client_id = json_data["client_id"]
            object.user_id = json_data["user_id"]
            object.parent_id = json_data["parent_id"]
            fields = json_data["fields"]
            object.update_date = datetime.datetime.now()
            obj = object_model.Object(parent_id=object.parent_id, fields=fields)
            object.data = encoder.encode(obj)

            session.add(object)
            session.commit()
            return object, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Entity")



