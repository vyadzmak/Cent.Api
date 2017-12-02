import json
import modules.json_modules.json_encoder as encoder
import models.app_models.dynamic_object_models.dynamic_object_model as d_object
from models.db_models.models import Schemas,Objects
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_converters.schema_data_converter as s_d_converter
import models.app_models.schema_models.schema_model as s_model
import datetime
from sqlalchemy import and_
import copy
def get_to_schema_link_items(id,f_name):
    try:
        schema = session.query(Schemas).filter(Schemas.id == id).first()

        j = json.loads(schema.data)
        fields = j["fields"]
        index_name =""
        val_name =""

        cat_id =-1
        for f in fields:

            if (f["name"]==f_name ):
                var = f["var"]["schema_id"]

                cat_id=var

        return get_to_schema_catalog_items(cat_id)
    except Exception as e:
        return None


def get_to_schema_catalog_items(id):
    schema = session.query(Schemas).filter(Schemas.id == id).first()

    j = json.loads(schema.data)
    fields = j["fields"]
    index_name =""
    val_name =""


    for f in fields:
        if (f["is_value"]==True and val_name==""):
            val_name = f["name"]
        if (f["is_index"] == True and index_name == ""):
            index_name = f["name"]

    objects = session.query(Objects).filter(Objects.schema_id == id).all()
    items =[]


    for ob in objects:
        f_data = json.loads(ob.data)
        ob_fields =f_data["fields"]
        index =""
        val =""

        for o_f in ob_fields:
            if (o_f["name"]==val_name):
                val = o_f["output_value"]

            if (o_f["name"]==index_name):
                index = o_f["output_value"]

        if (index!="" and val!=""):
            item = d_object.DynamicObject()
            setattr(item,"id",index)
            setattr(item,"name",val)
            items.append(item)
    return items

    p=0


def get_to_data_field_items(data):
    try:
        j = json.loads(data)
        fields = j["fields"]

        for field in fields:
            field_type = field["field_type"]
            if (field_type==9 or field_type==5):
               items = get_to_schema_catalog_items(field["var"]["schema_id"])
               if (items!=None and len(items)>0):
                   field["items"] = encoder.encode(items)
        j["fields"] =fields
        data =encoder.encode(j)
        return data
    except Exception as e:
        return data
