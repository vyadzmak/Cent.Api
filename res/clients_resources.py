from models.db_models.models import Clients
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
client_info_fields = {
    'id': fields.Integer,
    'client_id': fields.Integer,
    'logo_attachment_id': fields.Integer,
    'address': fields.String,
    'main_phone_number': fields.String,
    'additional_phone_number': fields.String,
    'site_url': fields.String,
    'main_info': fields.String,
    'additional_info': fields.String,
    'email': fields.String,
    'location_coordinates': fields.List(fields.Float)
}
client_type_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}

client_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_date': fields.DateTime,
    'registration_number': fields.String,
    'lock_state': fields.Boolean,
    'client_type_id': fields.Integer,
    'client_type': fields.Nested(client_type_fields),
    'client_info':fields.Nested(client_info_fields)
}


class ClientResource(Resource):
    @marshal_with(client_fields)
    def get(self, id):
        client = session.query(Clients).filter(Clients.id == id).first()
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        return client

    def delete(self, id):
        try:
            client = session.query(Clients).filter(Clients.id == id).first()
            if not client:
                abort(404, message="Client type {} doesn't exist".format(id))
            session.delete(client)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Client")

    @marshal_with(client_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            client = session.query(Clients).filter(Clients.id == id).first()
            client.name = json_data['name']
            client.registration_number = json_data["registration_number"]
            client.lock_state = json_data["lock_state"]
            client.client_type_id = json_data["client_type_id"]
            session.add(client)
            session.commit()
            return client, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Client")


class ClientListResource(Resource):
    @marshal_with(client_fields)
    def get(self):
        clients = session.query(Clients).all()
        return clients

    @marshal_with(client_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            client = Clients(name=json_data["name"], registration_number=json_data["registration_number"],
                             lock_state=json_data["lock_state"], client_type_id=json_data["client_type_id"])
            session.add(client)
            session.commit()
            return client, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Client")
