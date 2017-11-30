from enum import Enum
class FieldType(Enum):
    STRING=0
    INT =1,
    FLOAT = 2,
    DATETIME=3,
    ADDRESS=4,
    LINK = 5,
    BOOLEAN = 6,
    BACKREF = 7,
    DICT = 8,
    CATALOG = 9,
    SINGLE_IMAGE = 10,
    IMAGES =11


# self.init_variable(0,"STRING","Текстовая переменная",s_var.StringVar() )
#         self.init_variable(1,"INT","Переменная целочисленного типа",i_var.IntVar())
#         self.init_variable(2,"FLOAT","Переменная с плавающей точкой",f_var.FloatVar())
#         self.init_variable(3,"DATETIME","Дата",d_var.DateVar())
#         self.init_variable(4,"ADDRESS","Адрес",a_var.AddressVar())
#         self.init_variable(5,"LINK","Переменная ссылочного типа",l_var.LinkVar())
#         self.init_variable(6,"BOOLEAN","Переменная логического типа",b_var.BooleanVar())
#         self.init_variable(7, "BACKREF", "Переменная обратной ссылки",None, True)
#         self.init_variable(8, "DICT", "Словарь",None, True)
#         self.init_variable(9, "CATALOG", "Справочник",c_var.CatalogVar())
#         self.init_variable(10, "SINGLE_IMAGE", "Единичное изображение",None, True)
#         self.init_variable(11, "IMAGES", "Галлерея изображений",None, True)
#field for object
class Field():
    def __init__(self,obj_len,name,title,field_type, field_var,is_index=False,is_value=False, inherited=False):
        self.index =obj_len+1
        self.title = title
        self.name =name
        self.field_type =field_type
        self.var =field_var
        self.value =""
        self.inherited =inherited
        self.is_index =is_index
        self.is_value = is_value
        pass




