import modules.db_converters.output_value_converter as output_value_converter
#поля объекта
class ObjectField():
    def __init__(self,index,type, name, title, value, var):
        self.index = index
        self.field_type= type
        self.name =name
        self.title = title
        self.value =value
        self.output_value = output_value_converter.convert_output_value(type,var,value)
        self.output_value = value
        self.items = []
        pass


class Object():
    def __init__(self,parent_id, fields):
        self.parent_id =parent_id
        self.fields =[]
        self.init_fields(fields)


        pass

    def init_fields(self,fields):
        for field in fields:
            self.fields.append(ObjectField(field["index"],field["field_type"],field["name"],field["title"],field["value"],field["var"]))
        pass