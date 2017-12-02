import models.app_models.dynamic_object_models.dynamic_object_model as dynamic_object
import models.app_models.dynamic_table_models.dynamic_table_model as dynamic_table
import json
import modules.json_modules.json_encoder as encoder
import modules.db_converters.field_items_converter as f_i_converter
def get_to_schema(id):
    from models.db_models.models import Schemas
    from db.db import session

    schema = session.query(Schemas).filter(Schemas.id==id).first()
    return schema
    pass
def check_field(arr,name):
    try:
        return arr[name]
    except:
        return True


def generate_dynamic_table_by_objects(objects):
    try:
        if (len(objects)==0):
            return None

        dt = dynamic_table.DynamicTable()

        #generate header
        for ob in objects:
            # data =ob.data
            # data =  json.loads(data)
            # fields =data["fields"]
            schema_id =ob.schema_id
            #schema_id =data["schema_id"]
            sch = get_to_schema(schema_id)
            data = sch.data
            data = json.loads(data)
            fields = data["fields"]
            for field in fields:
                if (check_field(field,"is_visible")):
                    dt.init_header_element(text=field["title"],align="center",value=field["name"])

            break

        for ob in objects:
            items = {}
            data = ob.data
            data = json.loads(data)
            fields = data["fields"]
            d_obj = dynamic_object.DynamicObject()
            setattr(d_obj, "g_id", ob.id)
            for field in fields:
                field_type = field["field_type"]
                if (field_type == 9 ):
                    items = f_i_converter.get_to_schema_link_items(ob.schema_id,field["name"])
                    if (items != None and len(items) > 0):
                        field["items"] = encoder.encode(items)
                        o_v = field["output_value"]
                        for i in items:
                            if (str(i.id)==str(o_v)):
                                field["output_value"] =i.name
                                break


                if (check_field(field,"is_visible")):

                    setattr(d_obj, field["name"], field["output_value"])

            dt.init_item(d_obj)
        return  encoder.encode(dt)

    except Exception as e:
        return None

