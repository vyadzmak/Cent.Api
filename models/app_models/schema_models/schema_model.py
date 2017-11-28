import models.app_models.variable_models.var_description_model as v_description

class Schema():
    def __init__(self, name, title, group_title="", is_catalog=False, is_update=False):
        self.fields = []
        self.name = name
        self.title = title
        self.group_title = title
        self.is_catalog = is_catalog

        self.var_descritpions = v_description.VarDescriptions()

        if (group_title != ""):
            self.group_title = group_title

    def init_field(self, field):
        self.fields.append(field)
        pass

    # init fields by template
    def init_fields(self, fields):
        for field in fields:
            self.init_field(field)
        pass

    # set field value
    def set_field_value(self, name, value):
        r = [f for f in self.fields if f.name == name]
        if (len(r) > 0):
            r[0].value = value

    # get field value
    def get_field_value(self, name, value):
        pass
