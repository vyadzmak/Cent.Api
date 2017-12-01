
from db.db import session


def get_objects_by_schema_id(id):
    try:
        from models.db_models.models import Objects
        objects = session.query(Objects).filter(Objects.schema_id == id).all()
        return objects
    except Exception as e:
        return None