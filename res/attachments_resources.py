from models.db_models.models import Attachments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

attachment_type_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,
    'extensions': fields.List(fields.String)
}

user_login_fields = {
    'login': fields.String,
}

user_data = {
    'id': fields.Integer(attribute="id"),
    'first_name': fields.String(attribute="first_name"),
    'last_name': fields.String(attribute="last_name"),
    'login_data': fields.Nested(user_login_fields)
}

attachments_fields = {
    'id': fields.Integer,
    'original_file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Integer,
    'uid': fields.String,
    'attachment_type_id': fields.Integer,
    'user_creator_id': fields.Integer,
    'upload_date': fields.DateTime,
    'attachment_user_data':fields.Nested(user_data),
    'attachment_type_data':fields.Nested(attachment_type_fields)
}

parser = reqparse.RequestParser()


class AttachmentsResource(Resource):
    @marshal_with(attachments_fields)
    def get(self, id):
        attachment = session.query(Attachments).filter(Attachments.id == id).first()
        if not attachment:
            abort(404, message="Attachment  {} doesn't exist".format(id))
        return attachment

    def delete(self, id):
        try:
            attachment = session.query(Attachments).filter(Attachments.id == id).first()
            if not attachment:
                abort(404, message="Attachment  {} doesn't exist".format(id))
            session.delete(attachment)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Attachment ")

    @marshal_with(attachments_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            attachment = session.query(Attachments).filter(Attachments.id == id).first()
            # original_file_name, file_path, file_size,attachment_type_id,user_creator_id
            attachment.original_file_name = json_data['original_file_name']
            attachment.file_path = json_data['file_path']
            attachment.file_size = json_data['file_size']
            attachment.attachment_type_id = json_data['attachment_type_id']
            attachment.user_creator_id = json_data['user_creator_id']
            session.add(attachment)
            session.commit()
            return attachment, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Attachment Type")


class AttachmentsListResource(Resource):
    @marshal_with(attachments_fields)
    def get(self):
        attachment = session.query(Attachments).all()
        return attachment

    @marshal_with(attachments_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # original_file_name, file_path, file_size,attachment_type_id,user_creator_id
            attachment = Attachments(original_file_name=json_data["original_file_name"], file_path=json_data["file_path"],
                                     file_size=json_data["file_size"],
                                     attachment_type_id=json_data["attachment_type_id"],
                                     user_creator_id=json_data["user_creator_id"]
                                     )
            session.add(attachment)
            session.commit()
            return attachment, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Attachment")
