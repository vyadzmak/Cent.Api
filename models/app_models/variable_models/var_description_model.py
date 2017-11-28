import models.app_models.variable_models.boolean_variable_model as b_var
import models.app_models.variable_models.date_variable_model as d_var
import models.app_models.variable_models.float_variable_model as f_var
import models.app_models.variable_models.int_variable_model as i_var
import models.app_models.variable_models.string_variable_model as s_var
import models.app_models.variable_models.address_variable_model as a_var
import models.app_models.variable_models.link_variable_model as l_var
import models.app_models.variable_models.catalog_variables_model as c_var

class VarDescription():
    def __init__(self,id,name,title,var=None,not_used=False):
        self.id = id
        self.name = name
        self.title = title
        self.var = var
        self.not_used = not_used
        pass


class VarDescriptions():
    def __init__(self):
        self.variables = []
        self.init_variables()

    def init_variable(self,id,name,title,var=None,not_used=False):
        self.variables.append(VarDescription(id, name, title,var,not_used))


    def init_variables(self):
        self.init_variable(0,"STRING","Текстовая переменная",s_var.StringVar() )
        self.init_variable(1,"INT","Переменная целочисленного типа",i_var.IntVar())
        self.init_variable(2,"FLOAT","Переменная с плавающей точкой",f_var.FloatVar())
        self.init_variable(3,"DATETIME","Дата",d_var.DateVar())
        self.init_variable(4,"ADDRESS","Адрес",a_var.AddressVar())
        self.init_variable(5,"LINK","Переменная ссылочного типа",l_var.LinkVar())
        self.init_variable(6,"BOOLEAN","Переменная логического типа",b_var.BooleanVar())
        self.init_variable(7, "BACKREF", "Переменная обратной ссылки",None, True)
        self.init_variable(8, "DICT", "Словарь",None, True)
        self.init_variable(9, "CATALOG", "Справочник",c_var.CatalogVar())
        self.init_variable(10, "SINGLE_IMAGE", "Единичное изображение",None, True)
        self.init_variable(11, "IMAGES", "Галлерея изображений",None, True)
        pass