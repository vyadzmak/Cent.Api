import models.app_models.dynamic_object_models.dynamic_object_model as dynamic_object
import models.app_models.dynamic_table_models.dynamic_table_model as dynamic_table


def generate_dynamic_table_by_objects(objects):
    try:
        if (len(objects)):
            return None

        dt = dynamic_table.DynamicTable()

        #generate header
        for ob in objects:
            for field in ob.field:
                dt.init_header_element(text=field.title,align='center',value=field.name)

            break



        for ob in objects:
            items = []
            for field in ob.fields:
                d_obj = dynamic_object.DynamicObject()
                #d_obj.




        return None

    except Exception as e:
        return None

