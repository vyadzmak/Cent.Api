import models.app_models.field_models.field_model as field_model
import models.app_models.variable_models.boolean_variable_model as b_var
import models.app_models.variable_models.date_variable_model as d_var
import models.app_models.variable_models.float_variable_model as f_var
import models.app_models.variable_models.int_variable_model as i_var
import models.app_models.variable_models.string_variable_model as s_var
import models.app_models.variable_models.var_description_model as v_description
import models.app_models.variable_models.general_var_models as g_model

import uuid

class Object():
    def __init__(self, name, title, group_title="", is_catalog=False,is_update=False):
        self.fields =[]
        self.name = name
        self.title = title
        self.group_title = title
        self.is_catalog = is_catalog

        self.u_id =str(uuid.uuid4())
        #self.var_descritpions = v_description.VarDescriptions()
        if (is_update==False):
            self.init_field(
                field_model.Field(len(self.fields), "name", "Наименование", field_model.FieldType.STRING.value,
                                  s_var.StringVar(not_null=True, min_length=3, max_length=10)))

        if (group_title!= ""):
            self.group_title = group_title

    def init_field(self,field):
        self.fields.append(field)
        pass

    #init fields by template
    def init_fields(self,fields):
        for field in fields:
            self.init_field(field)
        pass

    #set field value
    def set_field_value(self,name,value):
        r = [f for f in self.fields if f.name==name]
        if (len(r)>0):
             r[0].value= value


    #get field value
    def get_field_value(self,name,value):
        pass