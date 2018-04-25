from flask import Flask
from flask_restful import Resource, Api
from models.app_models.json_encoder_models.json_encoder import AlchemyEncoder
from flask_cors import CORS
from flask_basicauth import BasicAuth
#init application
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'cent_user'
app.config['BASIC_AUTH_PASSWORD'] = 'vPe0N9zb7bGK1Ng5'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)
#cors = CORS(app, resources={r"/login/*": {"origins": "*"}})
CORS(app)

app.config['BUNDLE_ERRORS'] = True
json_encoder = AlchemyEncoder
app.json_encoder =json_encoder
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['PROPAGATE_EXCEPTIONS'] = True



@app.errorhandler(500)
def internal_error(error):
    return "500 error"
api = Api(app)
#import resources
from res.user_roles_resources import *
from res.client_types_resources import *
from res.clients_resources import *
from res.users_resources import *
from res.user_logins_resources import *
from res.log_resources import *
from res.upload_resources import *
from res.schemas_resources import *
from res.object_resources import *
from res.entity_resources import *
from res.action_log_types_resources import *
from res.action_log_resources import *
from res.attachment_types_resources import *
from res.attachments_resources import *
from res.client_info_resources import *
#add resources
#user roles
api.add_resource(UserRoleListResource, '/userRoles', endpoint='user-roles')
api.add_resource(UserRoleResource, '/userRole/<int:id>', endpoint='user-role')
api.add_resource(AdminUserRoleListResource, '/adminUserRoles', endpoint='admin-user-role')

#client types
api.add_resource(ClientTypeListResource, '/clientTypes', endpoint='client-types')
api.add_resource(ClientTypeResource, '/clientTypes/<int:id>', endpoint='client-type')

#clients
api.add_resource(ClientListResource, '/clients', endpoint='clients')
api.add_resource(ClientResource, '/clients/<int:id>', endpoint='client')

#users
api.add_resource(ClientUsersListResource, '/clientUsers/<int:id>', endpoint='client-users')


api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/user/<int:id>', endpoint='user')

#user logins
api.add_resource(UserLoginListResource, '/userLogins', endpoint='usersLogins')
api.add_resource(UserLoginResource, '/userLogin/<int:id>', endpoint='userLogin')
api.add_resource(UserAuthResource, '/login', endpoint='login')

#log
api.add_resource(LogListResource, '/log', endpoint='log')

#upload files
api.add_resource(UploadFile, '/upload', endpoint='upload')

#schemas
api.add_resource(SchemaListResource, '/schemas', endpoint='schemas')
api.add_resource(SchemaTypesListResource, '/schemaTypes', endpoint='schemasTypes')
api.add_resource(SchemaResource, '/schema/<int:id>', endpoint='schema')

#get to all schema catalogs
api.add_resource(SchemaCatalogsListResource, '/schemaCatalogs/<int:clientId>', endpoint='schemaCatalogs')

#get to all schema links
api.add_resource(SchemaLinkListResource, '/schemaLinks/<int:clientId>', endpoint='schemaLinks')

#get to all main schemas by Client
api.add_resource(SchemaClientListResource, '/schemaClients/<int:clientId>', endpoint='schemaClients')

#get to full schemas by Client
api.add_resource(FullSchemaClientListResource, '/fullSchemaClients/<int:clientId>', endpoint='fullSchemaClients')


#objects
#get to all objects
api.add_resource(ObjectListResource, '/objects', endpoint='objects')

#get to object
api.add_resource(ObjectResource, '/object/<int:id>', endpoint='object')

#get to schema objects
api.add_resource(ObjectSchemaListResource, '/schemaObjects/<int:schemaId>', endpoint='schemaObjects')

#entity objects
api.add_resource(ObjectEntitySchemaListResource, '/entityObjects', endpoint='entityObjects')


api.add_resource(EntityResource, '/entityDetails/<int:id>', endpoint='entityDetails')

api.add_resource(TestResource, '/test', endpoint='tests')


#action log type
api.add_resource(ActionLogTypeListResource, '/actionLogTypes', endpoint='actionLogTypes')
api.add_resource(ActionLogTypeResource, '/actionLogTypes/<int:id>', endpoint='actionLogType')

#action log
api.add_resource(ActionLogListResource, '/actionLog', endpoint='actionLogs')
api.add_resource(ActionLogResource, '/actionLog/<int:id>', endpoint='actionLog')

#attachment log type
api.add_resource(AttachmentTypeListResource, '/attachmentTypes', endpoint='attachmentTypes')
api.add_resource(AttachmentTypeResource, '/attachmentTypes/<int:id>', endpoint='attachmentType')

#attachments
api.add_resource(AttachmentsListResource, '/attachments', endpoint='attachments')
api.add_resource(AttachmentsResource, '/attachments/<int:id>', endpoint='attachment')

#client info
api.add_resource(ClientInfoListResource, '/clientInfo', endpoint='clientInfos')
api.add_resource(ClientInfoResource, '/clientInfo/<int:id>', endpoint='clientInfo')
#start application
if __name__ == '__main__':
    #u_s.get_user_roles()
    app.run(debug=True)