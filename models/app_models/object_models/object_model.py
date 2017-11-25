import models.app_models.field_models.field_model as field_model
import models.app_models.variable_models.boolean_variable_model as b_var
import models.app_models.variable_models.date_variable_model as d_var
import models.app_models.variable_models.float_variable_model as f_var
import models.app_models.variable_models.int_variable_model as i_var
import models.app_models.variable_models.string_variable_model as s_var


class Object():
    def __init__(self, name,title):
        self.fields =[]
        self.name = name
        self.title = title

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