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
import datetime

Base = declarative_base()

# user table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    message = Column('message', String)

    def __init__(self, message):
        self.date = datetime.datetime.now()
        self.message = message


# user table
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

    def __init__(self,login,password,user_id):
        self.login = login
        self.password = password
        self.user_id = user_id
        self.registration_date = datetime.datetime.now()
    pass


# client type
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




if __name__ == "__main__":
    from sqlalchemy import create_engine
    from models.app_models.setting_models.setting_model import DB_URI

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
