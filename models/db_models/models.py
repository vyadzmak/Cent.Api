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

import models.app_models.schema_models.schema_model as schema_model
import models.app_models.object_models.object_model as object_model
import modules.json_modules.json_encoder as encoder
import datetime

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

    def __init__(self, action_type_id, user_id, message=''):
        self.action_type_id = action_type_id
        self.action_date = datetime.datetime.now()
        self.message = message

        # action_types


class ActionLogTypes(Base):
    __tablename__ = 'action_types'
    id = Column(Integer, primary_key=True)

    message = Column('message', String(750))
    code = Column('code', Integer)

    def __init__(self, message, code=-1):
        self.message = message
        self.code = code

        # attachment_types
        # attachments
        # client_info


# main section
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from models.app_models.setting_models.setting_model import DB_URI

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
