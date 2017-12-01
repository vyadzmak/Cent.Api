from db.db import session
def get_schema_by_id(id):
    try:
        from models.db_models.models import Schemas
        schema = session.query(Schemas).filter(Schemas.id == id).first()
        return schema
    except Exception as e:
        return None