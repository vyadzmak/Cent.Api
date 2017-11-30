import json
import modules.json_modules.json_encoder as encoder

from models.db_models.models import Schemas
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_converters.schema_data_converter as s_d_converter
import models.app_models.schema_models.schema_model as s_model
import datetime
from sqlalchemy import and_
import copy


def get_to_data_field_items(data):
    try:
        j = json.loads(data)
        fields = j["fields"]
        for field in fields:
            field_type = field["field_type"]
            if (field_type==9):
                p =0
        return data
    except Exception as e:
        return data
