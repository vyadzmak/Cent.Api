from db.db import session
import json
import models.app_models.dynamic_object_models.dynamic_object_model as d_object
def get_entity_fields_by_id(id):
    from models.db_models.models import Objects
    object = session.query(Objects).filter(Objects.id == id).first()
    return object.data
    pass


def get_items(object_id, type_id):
    from models.db_models.models import Schemas
    from models.db_models.models import Objects
    items = []
    object = session.query(Objects).filter(Objects.id ==object_id).first()

    schema= session.query(Schemas).filter(Schemas.id==object.schema_id).first()

    data = json.loads(schema.data)
    fields = data["fields"]

    for f in fields:
        if (f["field_type"]==5):
            v = f["var"]
            id =v["schema_id"]
            nm =v["title"]

            t_schema = session.query(Schemas).filter(Schemas.id==id).first()
            if (t_schema.schema_type_id==type_id):
                ob = d_object.DynamicObject()
                setattr(ob, 'id', id)
                setattr(ob, 'name', nm)
                items.append(ob)
    return items
pass

