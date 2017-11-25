from enum import Enum
class FieldType(Enum):
    STRING=1
    INT =2,
    FLOAT = 3,
    BOOLEAN=4,
    DATE=5


#field for object
class Field():
    def __init__(self,obj_len,name,title,field_type, field_var):
        self.index =obj_len+1
        self.title = title
        self.name =name
        self.field_type =field_type
        self.var =field_var
        self.value =""

        pass




