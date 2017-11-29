import models.app_models.variable_models.var_description_model as v_description
from enum import Enum

class SchemaType():
    def __init__(self,id,name,title):
        self.id = id
        self.name = name
        self.title = title

class Schema():
    def __init__(self, name, title, group_title="", schema_type_id=0, is_update=False):
        self.fields = []
        self.name = name
        self.title = title
        self.group_title = title

        self.var_descritpions = v_description.VarDescriptions()
        self.schema_type_id =schema_type_id
        self.schema_types =[]

        self.init_schema_types()
        if (group_title != ""):
            self.group_title = group_title

    def init_schema_type(self,id,name,title):
        self.schema_types.append(SchemaType(id,name,title))

    def init_schema_types(self):
        self.init_schema_type(0,'OBJECT','Объект')
        self.init_schema_type(1,'SUBJECT','Субъект')
        self.init_schema_type(2,'DOCUMENT','Документ')
        self.init_schema_type(3,'CATALOG','Справочник')

    def init_field(self, field):
        self.fields.append(field)
        pass

    # init fields by template
    def init_fields(self, fields):
        for field in fields:
            self.init_field(field)
        pass

    # set field value
    def set_field_value(self, name, value):
        r = [f for f in self.fields if f.name == name]
        if (len(r) > 0):
            r[0].value = value

    # get field value
    def get_field_value(self, name, value):
        pass
