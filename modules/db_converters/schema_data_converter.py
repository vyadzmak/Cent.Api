import modules.json_modules.json_encoder as encoder
import models.app_models.object_models.object_model as ob_model
import models.app_models.field_models.field_model as field_model

import models.app_models.variable_models.boolean_variable_model as b_var
import models.app_models.variable_models.date_variable_model as d_var
import models.app_models.variable_models.float_variable_model as f_var
import models.app_models.variable_models.int_variable_model as i_var
import models.app_models.variable_models.string_variable_model as s_var
import models.app_models.variable_models.address_variable_model as a_var
import models.app_models.variable_models.link_variable_model as l_var
import models.app_models.variable_models.catalog_variables_model as c_var

import json
def init_field(field,field_type):
    v = field["var"]
    #string
    if (field_type==0):
        return s_var.StringVar(v["not_null"],v["default_value"],v["max_length"],v["min_length"],v["input_format"],v["output_format"])
        pass

        # int
    if (field_type == 1):
        return i_var.IntVar(v["not_null"],v["default_value"],v["max_value"],v["min_value"])
        pass

        # float
    if (field_type == 2):
        return f_var.FloatVar(v["not_null"],v["default_value"],v["max_value"],v["min_value"],v["round_count"],v["separator"])
        pass

        # DATETIME
    if (field_type == 3):
        return d_var.DateVar(v["output_format"],v["not_null"])
        pass

        # ADDRESS
    if (field_type== 4):
        return a_var.AddressVar(v["address"],v["lat"],v["long"])
        pass

        # LINK
    if (field_type == 5):
        return l_var.LinkVar(v["title"],v["uid"])
        pass

        # BOOLEAN
    if (field_type== 6):
        return b_var.BooleanVar(v["not_null"],v["default_value"],v["false_value"],v["true_value"])
        pass

        # BACKREF
    if (field_type== 7):
        return None
        pass

        # DICT
    if (field_type == 8):
        return None
        pass

        # CATALOG
    if (field_type == 9):
        return c_var.CatalogVar(v["title"],v["uid"],v["selected_id"])
        pass

        # SINGLE_IMAGE
    if (field_type == 10):
        return None
        pass

        # images
    if (field_type ==11):
        return None
        pass


    pass


def convert_schema_object(json_data):
    name = json_data['name']
    title = json_data["title"]
    group_title = json_data["group_title"]
    is_catalog = json_data["is_catalog"]
    data= json_data["data"]


    fields= json.loads(data)["fields"]
    ob = ob_model.Object(name,title,group_title,is_catalog,True)
    ob.fields =[]

    for field in fields:
        field_type = field["field_type"]
        f_var = init_field(field,field_type)

        r_field = field_model.Field(len(ob.fields),field["name"], field["title"], field_type,f_var)
        ob.init_field(r_field)
    return encoder.encode(ob)
    pass