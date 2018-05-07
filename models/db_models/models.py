from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime

from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, String, Column, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
import uuid
import models.app_models.schema_models.schema_model as schema_model
import models.app_models.object_models.object_model as object_model
import modules.json_modules.json_encoder as encoder
import datetime
from geoalchemy2 import Geometry

Base = declarative_base()


# log table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    message = Column('message', String)

    def __init__(self, message):
        self.date = datetime.datetime.now()
        self.message = message


# users table
class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    lock_state = Column('lock_state', Boolean)
    client_id = Column('client_id', ForeignKey('clients.id'))
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    user_data = relationship("UserLogins", backref="user_data")

    def __init__(self, first_name, last_name, lock_state, client_id, user_role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.lock_state = lock_state
        self.client_id = client_id
        self.user_role_id = user_role_id


# user roles
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    users = relationship("Users", backref="user_role")

    def __init__(self, name):
        self.name = name


# user logins
class UserLogins(Base):
    __tablename__ = 'user_logins'
    id = Column('id', Integer, primary_key=True)
    login = Column('login', String)
    password = Column('password', String)
    token = Column('token', String)
    registration_date = Column('registration_date', DateTime)
    last_login_date = Column('last_login_date', DateTime, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    user_login_data = relationship("Users", backref="login_data")

    def __init__(self, login, password, user_id):
        self.login = login
        self.password = password
        self.user_id = user_id
        self.registration_date = datetime.datetime.now()

    pass


# client types
class ClientTypes(Base):
    __tablename__ = 'client_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    clients = relationship("Clients", backref="client_type")


# clients
class Clients(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(70))
    registration_date = Column('registration_date', DateTime)
    registration_number = Column('registration_number', String(25))
    lock_state = Column('lock_state', Boolean)
    client_type_id = Column('client_type_id', ForeignKey('client_types.id'))
    user_client = relationship("Users", backref="client")
    client_info = relationship('ClientInfo', backref="client_info")

    def __init__(self, name, registration_number, lock_state, client_type_id):
        self.name = name
        self.registration_number = registration_number
        self.lock_state = lock_state
        self.client_type_id = client_type_id
        self.registration_date = datetime.datetime.now()


# schemas
class Schemas(Base):
    __tablename__ = 'schemas'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(32))
    title = Column('title', String(32))
    group_title = Column('group_title', String(32))
    description = Column('description', String(500))
    schema_type_id = Column('schema_type_id', Integer)
    data = Column(JSON)
    client_id = Column('client_id', ForeignKey('clients.id'))
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    update_date = Column('update_date', DateTime)
    is_show = Column('is_show', Boolean)

    def __init__(self, name, title, group_title, description, schema_type_id, client_id, user_id, is_show):
        self.name = name
        self.title = title
        self.group_title = group_title
        self.description = description
        self.schema_type_id = schema_type_id
        self.client_id = client_id
        self.user_id = user_id
        self.creation_date = datetime.datetime.now()
        self.is_show = is_show
        obj = schema_model.Schema(name, title, group_title, schema_type_id)
        self.creation_date = datetime.datetime.now()
        self.update_date = datetime.datetime.now()
        self.data = encoder.encode(obj)


# objects
class Objects(Base):
    __tablename__ = 'objects'
    id = Column('id', Integer, primary_key=True)
    data = Column(JSON)
    client_id = Column('client_id', ForeignKey('clients.id'))
    schema_id = Column('schema_id', ForeignKey('schemas.id'))
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    update_date = Column('update_date', DateTime)
    parent_id = Column('parent_id', Integer)

    def __init__(self, schema_id, client_id, user_id, parent_id, fields):
        self.client_id = client_id
        self.user_id = user_id
        self.schema_id = schema_id
        self.creation_date = datetime.datetime.now()
        self.update_date = datetime.datetime.now()
        self.parent_id = parent_id
        obj = object_model.Object(parent_id=parent_id, fields=fields)
        self.data = encoder.encode(obj)

        # NEW MODELS


# action_log
class ActionLog(Base):
    __tablename__ = 'action_log'
    id = Column(Integer, primary_key=True)
    action_type_id = Column('action_type_id', ForeignKey('action_types.id'))
    action_date = Column('action_date', DateTime)
    user_id = Column('user_id', ForeignKey('users.id'))
    message = Column('message', String(750))
    action_log_type = relationship('ActionLogTypes', backref='action_log_type')
    user_data = relationship('Users', backref="action_log_user_data")

    def __init__(self, action_type_id, user_id, message=''):
        self.action_type_id = action_type_id
        self.action_date = datetime.datetime.now()
        self.message = message
        self.user_id = user_id
        # action_types


# action_log types
class ActionLogTypes(Base):
    __tablename__ = 'action_types'
    id = Column(Integer, primary_key=True)

    message = Column('message', String(750))
    code = Column('code', Integer)

    def __init__(self, message, code=-1):
        self.message = message
        self.code = code


# attachment_types
class AttachmentTypes(Base):
    __tablename__ = 'attachment_types'
    id = Column(Integer, primary_key=True)

    name = Column('name', String(128))
    title = Column('title', String(128))
    extensions = Column(postgresql.ARRAY(String))

    def __init__(self, name, title, extensions):
        self.name = name
        self.title = title
        self.extensions = extensions


# attachments
class Attachments(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)

    original_file_name = Column('original_file_name', String(256))
    file_path = Column('file_path', String(256))
    file_size = Column('file_size', Integer)
    uid = Column('uid', String(64))
    attachment_type_id = Column('attachment_type_id', ForeignKey('attachment_types.id'))
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    upload_date = Column('upload_date', DateTime)

    attachment_user_data = relationship('Users', backref="attachment_user_data")
    attachment_type_data = relationship('AttachmentTypes', backref="attachment_type_data")

    def __init__(self, original_file_name, file_path, file_size, attachment_type_id, user_creator_id):
        self.original_file_name = original_file_name
        self.file_path = file_path
        self.file_size = file_size
        self.attachment_type_id = attachment_type_id
        self.user_creator_id = user_creator_id
        self.uid = str(uuid.uuid4())
        self.upload_date = datetime.datetime.now()


# client_info
class ClientInfo(Base):
    __tablename__ = 'client_info'
    id = Column(Integer, primary_key=True)
    client_id = Column('client_id', ForeignKey('clients.id'))
    logo_attachment_id = Column('logo_attachment_id', ForeignKey('attachments.id'))
    address = Column('address', String(400))
    main_phone_number = Column('main_phone_number', String(32))
    additional_phone_number = Column('additional_phone_number', String(32))
    site_url = Column('site_url', String(32))
    main_info = Column('main_info', String(5500))
    additional_info = Column('additional_info', String(1500))
    email = Column('email', String(64))
    location_coordinates = Column(postgresql.ARRAY(Float))
    client_info_client = relationship('Clients', backref="client_info_client")

    def __init__(self, client_id, logo_attachment_id=None, address=None, main_phone_number=None,
                 additional_phone_number=None, site_url=None, main_info=None, additional_info=None, email=None,
                 location_coordinates=None):
        self.client_id = client_id
        self.logo_attachment_id = logo_attachment_id
        self.address = address
        self.main_phone_number = main_phone_number
        self.additional_phone_number = additional_phone_number
        self.site_url = site_url
        self.main_info = main_info
        self.additional_info = additional_info
        self.email = email
        self.location_coordinates = location_coordinates


# group_object_rights
class GroupObjectRights(Base):
    __tablename__ = 'group_object_rights'
    id = Column(Integer, primary_key=True)
    group_id = Column('group_id', ForeignKey('user_groups.id'))
    data = Column('data', JSON)
    updated_date = Column('updated_date', DateTime)
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    object_id = Column('object_id', ForeignKey('objects.id'))

    def __init__(self, group_id, user_creator_id, object_id, data=None):
        self.group_id = group_id
        self.user_creator_id = user_creator_id
        self.data = data
        self.updated_date = datetime.datetime.now()
        self.object_id = object_id


# user_groups
class UserGroups(Base):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True)
    created_date = Column('created_date', DateTime)
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    lock_state = Column('lock_state', Boolean)
    group_name = Column('group_name', String(64))
    group_members = Column(postgresql.ARRAY(Integer))
    user_group_user_data = relationship('Users', backref="user_group_user_data")

    def __init__(self, user_creator_id, group_name):
        self.user_creator_id = user_creator_id
        self.created_date = datetime.datetime.now()
        self.lock_state = False
        self.group_name = group_name
        self.group_members = []


# group_object_rights
class UserGroupSettings(Base):
    __tablename__ = 'user_group_settings'
    id = Column(Integer, primary_key=True)
    group_id = Column('group_id', ForeignKey('user_groups.id'))
    data = Column('data', JSON)
    user_group_data = relationship('UserGroups', backref="user_group_data")

    def __init__(self, group_id, data=None):
        self.group_id = group_id
        self.data = data


# object settings
class ObjectSettings(Base):
    __tablename__ = 'object_settings'
    id = Column(Integer, primary_key=True)
    object_id = Column('object_id', ForeignKey('objects.id'))
    data = Column('data', JSON)

    def __init__(self, object_id, data=None):
        self.object_id = object_id
        self.data = data


# object settings
class ObjectViews(Base):
    __tablename__ = 'object_views'
    id = Column(Integer, primary_key=True)
    object_id = Column('object_id', ForeignKey('objects.id'))
    data = Column('data', JSON)
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))

    def __init__(self, object_id, user_creator_id, data=None):
        self.object_id = object_id
        self.user_creator_id = user_creator_id
        self.data = data


# settings
class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    name = Column('name',String(256))
    value = Column('value',String(750))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    # shared group objects
class SharedGroupObjects(Base):
        __tablename__ = 'shared_group_objects'
        id = Column(Integer, primary_key=True)
        shared_date = Column('shared_date', DateTime)
        shared_user_id = Column('shared_user_id', ForeignKey('users.id'))
        lock_state = Column('lock_state', Boolean)
        object_id = Column('object_id', ForeignKey('objects.id'))
        #это ID групп, а не пользователей
        shared_members = Column(postgresql.ARRAY(Integer))
        def __init__(self, shared_user_id, object_id):
            self.shared_date = datetime.datetime.now()
            self.lock_state = False
            self.shared_user_id =shared_user_id
            self.object_id = object_id
            self.shared_members= []

        # shared group objects
class SharedUserObjects(Base):
            __tablename__ = 'shared_user_objects'
            id = Column(Integer, primary_key=True)
            shared_date = Column('shared_date', DateTime)
            shared_user_id = Column('shared_user_id', ForeignKey('users.id'))
            lock_state = Column('lock_state', Boolean)
            object_id = Column('object_id', ForeignKey('objects.id'))
            # это ID пользователей, а не групп
            shared_members = Column(postgresql.ARRAY(Integer))

            def __init__(self, shared_user_id, object_id):
                self.shared_date = datetime.datetime.now()
                self.lock_state = False
                self.shared_user_id = shared_user_id
                self.object_id = object_id
                self.shared_members = []

            # group_object_rights
class UserObjectRights(Base):
                __tablename__ = 'user_object_rights'
                id = Column(Integer, primary_key=True)
                user_id = Column('user_id', ForeignKey('users.id'))
                data = Column('data', JSON)
                updated_date = Column('updated_date', DateTime)
                user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
                object_id = Column('object_id', ForeignKey('objects.id'))

                def __init__(self, user_id, user_creator_id, object_id, data=None):

                    self.user_creator_id = user_creator_id
                    self.user_id = user_id
                    self.data = data
                    self.updated_date = datetime.datetime.now()
                    self.object_id = object_id

# object settings
class UserRouteAccess(Base):
                    __tablename__ = 'user_route_access'
                    id = Column(Integer, primary_key=True)

                    data = Column('data', JSON)
                    user_id = Column('user_id', ForeignKey('users.id'))
                    def __init__(self, user_id, data=None):
                        self.user_id = user_id
                        self.data = data
# main section
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from models.app_models.setting_models.setting_model import DB_URI

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
