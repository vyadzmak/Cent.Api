import models.app_models.dynamic_object_models.dynamic_object_model as dynamic_object
import models.app_models.dynamic_table_models.dynamic_table_model as dynamic_table
import json
import modules.json_modules.json_encoder as encoder
def generate_dynamic_table_by_objects(objects):
    try:
        if (len(objects)==0):
            return None



        dt = dynamic_table.DynamicTable()

        #generate header
        for ob in objects:
            data =ob.data
            data =  json.loads(data)
            fields =data["fields"]
            for field in fields:
                dt.init_header_element(text=field["title"],align="center",value=field["name"])

            break

        for ob in objects:
            items = []
            data = ob.data
            data = json.loads(data)
            fields = data["fields"]
            for field in fields:
                d_obj = dynamic_object.DynamicObject()
                setattr(d_obj, field["name"], field["output_value"])
                items.append(d_obj)
            dt.init_item(items)
        return  encoder.encode(dt)

    except Exception as e:
        return None

