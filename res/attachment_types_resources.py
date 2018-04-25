from models.db_models.models import AttachmentTypes
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

attachment_type_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,
    'extensions': fields.List(fields.String)
}

parser = reqparse.RequestParser()


class AttachmentTypeResource(Resource):
    @marshal_with(attachment_type_fields)
    def get(self, id):
        attachment_type = session.query(AttachmentTypes).filter(AttachmentTypes.id == id).first()
        if not attachment_type:
            abort(404, message="Attachment type {} doesn't exist".format(id))
        return attachment_type

    def delete(self, id):
        try:
            attachment_type = session.query(AttachmentTypes).filter(AttachmentTypes.id == id).first()
            if not attachment_type:
                abort(404, message="Attachment type {} doesn't exist".format(id))
            session.delete(attachment_type)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Attachment Type")

    @marshal_with(attachment_type_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            attachment_type = session.query(AttachmentTypes).filter(AttachmentTypes.id == id).first()
            attachment_type.name = json_data['name']
            attachment_type.title = json_data['title']
            attachment_type.extensions = json_data['extensions']
            session.add(attachment_type)
            session.commit()
            return attachment_type, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Attachment Type")


class AttachmentTypeListResource(Resource):
    @marshal_with(attachment_type_fields)
    def get(self):
        attachment_type = session.query(AttachmentTypes).all()
        return attachment_type

    @marshal_with(attachment_type_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # name, title, extensions
            attachment_type = AttachmentTypes(name=json_data["name"], title=json_data["title"],
                                              extensions=json_data["extensions"])
            session.add(attachment_type)
            session.commit()
            return attachment_type, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Attachment Type")
