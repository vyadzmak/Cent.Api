from db.db import session
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
    #s = session.query(Schemas).all()
    #o = session.query(Objects).all()
    elements = session.query(Objects, Schemas)\
        .filter(Objects.schema_id==Schemas.id)\
        .filter(Schemas.schema_type_id==type_id)\
        .filter(Objects.parent_id==object_id)\
        .all()
    indexes =[]
    for element in elements:
        ob = d_object.DynamicObject()
        sc = element[1]
        t = sc.id in indexes
        if (t ==False):
            indexes.append(sc.id)
            setattr(ob,'id',sc.id)
            setattr(ob,'name',sc.title)
            items.append(ob)

    return items



pass

#
# def get_objects_by_parent_id(parent_id):
#     from models.db_models.models import Objects
#     objects = session.query(Objects).filter(Objects.parent_id==parent_id).all()
#     return objects
#
# def get_objects_by_parent_id_and_type(parent_id,type_id):
#     from models.db_models.models import Objects
#     objects = session.query(Objects).filter(Objects.parent_id==parent_id).all()



#  return objects
