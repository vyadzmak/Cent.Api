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


def convert_address():
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
        # if (field_type == 5):
        #     return l_var.LinkVar(v["title"], v["schema_id"])
        #     pass
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
        # if (field_type == 9):
        #     return c_var.CatalogVar(v["title"], v["schema_id"], v["multi_select"])
        #     pass
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

    except Exception as e:
        return value

