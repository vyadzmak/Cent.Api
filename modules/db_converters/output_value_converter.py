import modules.db_helpers.schema_helper as schema_helper
import modules.db_helpers.object_helper as object_helper

import json

def convert_string(var,value):
    v=var
    not_null =v["not_null"]
    default_value =v["default_value"]
    max_length = v["max_length"]
    min_length = v["min_length"]
    input_format =v["input_format"]
    output_format =v["output_format"]
    return value
    pass

def convert_int():
    pass

def convert_float():
    pass

def convert_datetime():
    pass


def convert_address(var,value):
    pass

def convert_catalog(var,value):
    schema_id =var["schema_id"]
    schema = schema_helper.get_schema_by_id(schema_id)
    objects =object_helper.get_objects_by_schema_id(schema_id)
    if (objects==None or len(objects)==0):
        return value
    sj = json.loads(schema.data)

    val_name =""
    index =-1
    for f in sj["fields"]:
        if (f["is_value"]==True and val_name==""):
            val_name = f["name"]
            break

    for f in sj["fields"]:
        if (f["is_index"]==True and index==-1):
            index = f["index"]
            break
    p = 0
    for obj in objects:
        j = json.loads(obj.data)

        ex =False
        for f in j["fields"]:
            if (f["name"]=="id" and f["value"]==value):
                ex =True
                break

        if (ex==True):
            for f in j["fields"]:

                if (f["name"]==val_name):
                    return str(f["value"])
        p=p+1
    return value

    pass

def convert_output_value(field_type,var,value):
    try:
        # string
        if (field_type == 0):
            return convert_string(var,value)
            pass

        #     # int
        # if (field_type == 1):
        #     return i_var.IntVar(v["not_null"], v["default_value"], v["max_value"], v["min_value"])
        #     pass
        #
        #     # float
        # if (field_type == 2):
        #     return f_var.FloatVar(v["not_null"], v["default_value"], v["max_value"], v["min_value"], v["round_count"],
        #                           v["separator"])
        #     pass
        #
        #     # DATETIME
        # if (field_type == 3):
        #     return d_var.DateVar(v["not_null"], v["output_format"])
        #     pass
        #
        #     # ADDRESS
        # if (field_type == 4):
        #     return a_var.AddressVar(v["not_null"], v["max_length"])
        #     pass
        #
        #     # LINK
        if (field_type == 5):
            return convert_catalog(var,value)
            pass
        #
        #     # BOOLEAN
        # if (field_type == 6):
        #     return b_var.BooleanVar(v["not_null"], v["default_value"], v["false_value"], v["true_value"])
        #     pass
        #
        #     # BACKREF
        # if (field_type == 7):
        #     return None
        #     pass
        #
        #     # DICT
        # if (field_type == 8):
        #     return None
        #     pass
        #
        #     # CATALOG
        if (field_type == 9):
            return convert_catalog(var,value)
            pass
        #
        #     # SINGLE_IMAGE
        # if (field_type == 10):
        #     return None
        #     pass
        #
        #     # images
        # if (field_type == 11):
        #     return None
        #     pass
        return value
    except Exception as e:
        return value

