from models.db_models.models import ClientInfo
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

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
    'client_type': fields.Nested(client_type_fields)
    #'client_info':fields.Nested(client_info_fields)
}

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
    'zip_code': fields.String,
    'location_coordinates': fields.List(fields.Float),
    'client_info_client': fields.Nested(client_fields)

}

parser = reqparse.RequestParser()


class ClientInfoResource(Resource):
    @marshal_with(client_info_fields)
    def get(self, id):
        client_info = session.query(ClientInfo).filter(ClientInfo.id == id).first()
        if not client_info:
            abort(404, message="Attachment  {} doesn't exist".format(id))
        return client_info

    def delete(self, id):
        try:
            client_info = session.query(ClientInfo).filter(ClientInfo.id == id).first()
            if not client_info:
                abort(404, message="Attachment  {} doesn't exist".format(id))
            session.delete(client_info)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove Attachment ")

    @marshal_with(client_info_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            client_info = session.query(ClientInfo).filter(ClientInfo.id == id).first()
            client_info.client_id = json_data["client_id"]


            if ('logo_attachment_id' in json_data) == True:
                client_info.logo_attachment_id = json_data['logo_attachment_id']

            if ('address' in json_data) == True:
                client_info.address = json_data['address']

            if ('main_phone_number' in json_data) == True:
                client_info.main_phone_number = json_data['main_phone_number']

            if ('additional_phone_number' in json_data) == True:
                client_info.additional_phone_number = json_data['additional_phone_number']

            if ('site_url' in json_data) == True:
                client_info.site_url = json_data['site_url']

            if ('main_info' in json_data) == True:
                client_info.main_info = json_data['main_info']

            if ('additional_info' in json_data) == True:
                client_info.additional_info = json_data['additional_info']

            if ('email' in json_data) == True:
                client_info.email = json_data['email']

            if ('location_coordinates' in json_data) == True:
                client_info.location_coordinates = json_data['location_coordinates']

            if ('zip_code' in json_data) == True:
                client_info.zip_code = json_data['zip_code']

            session.add(client_info)
            session.commit()
            return client_info, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update Attachment Type")


class ClientInfoListResource(Resource):
    @marshal_with(client_info_fields)
    def get(self):
        client_info = session.query(ClientInfo).all()
        return client_info

    @marshal_with(client_info_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            # client_id,

            logo_attachment_id = None
            address = None
            main_phone_number = None,
            additional_phone_number = None
            site_url = None
            main_info = None
            additional_info = None
            email = None,
            location_coordinates = None
            zip_code = None

            if ('logo_attachment_id' in json_data) == True:
                logo_attachment_id = json_data['logo_attachment_id']

            if ('address' in json_data) == True:
                address = json_data['address']

            if ('main_phone_number' in json_data) == True:
                main_phone_number = json_data['main_phone_number']

            if ('additional_phone_number' in json_data) == True:
                additional_phone_number = json_data['additional_phone_number']

            if ('site_url' in json_data) == True:
                site_url = json_data['site_url']

            if ('main_info' in json_data) == True:
                main_info = json_data['main_info']

            if ('additional_info' in json_data) == True:
                additional_info = json_data['additional_info']

            if ('email' in json_data) == True:
                email = json_data['email']

            if ('location_coordinates' in json_data) == True:
                location_coordinates = json_data['location_coordinates']

            if ('zip_code' in json_data) == True:
                zip_code = json_data['zip_code']

            client_info = ClientInfo(json_data['client_id'], logo_attachment_id=logo_attachment_id, address=address,
                                     main_phone_number=main_phone_number,
                                     additional_phone_number=additional_phone_number, site_url=site_url,
                                     main_info=main_info, additional_info=additional_info, email=email,
                                     location_coordinates=location_coordinates,zip_code=zip_code)
            session.add(client_info)
            session.commit()
            return client_info, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record Attachment")
