import models.app_models.object_models.object_model as object_model
import modules.export_modules.exporter as exporter
import models.app_models.field_models.field_model as field_model
import copy
import models.app_models.variable_models.boolean_variable_model as b_var
import models.app_models.variable_models.date_variable_model as d_var
import models.app_models.variable_models.float_variable_model as f_var
import models.app_models.variable_models.int_variable_model as i_var
import models.app_models.variable_models.string_variable_model as s_var
import models.app_models.caatalog_models.catalog_model as catalog

def create_skin_type_catalog():
    skin_catalog =catalog.Catalog("Каталог цветов кожи")

    skin_object= object_model.Object("skin_object","Цвет кожи")
    skin_object.init_field(field_model.Field(len(skin_object.fields),"name","Наименование",field_model.FieldType.STRING,s_var.StringVar(not_null=True,min_length=3,max_length=32)))

    skins =['Белый','Черный','Желтый','Красный']



    for skin in skins:
        c_skin = copy.deepcopy(skin_object)
        c_skin.set_field_value("name", skin)
        skin_catalog.add_value(c_skin)

    return skin_catalog
    pass

def create_gender_type_object(genders):
    gender_catalog = catalog.Catalog("Каталог полов")

    gender_object = object_model.Object("gender_object", "Пол человека")
    gender_object.init_field(
        field_model.Field(len(gender_object.fields), "name", "Наименование", field_model.FieldType.STRING,
                          s_var.StringVar(not_null=True, min_length=3, max_length=10)))

    genders = ['Мужчина', 'Женщина']

    for gender in genders:
        c_skin = copy.deepcopy(gender_object)
        c_skin.set_field_value("name", gender)
        gender_catalog.add_value(c_skin)

    return gender_catalog
    pass

def create_race_catalog_object(races):
    pass



def create_test_object():
    objects =[]

    objects.append(create_skin_type_catalog())
    #obj = object_model.Object("human_obj","Объект человека")
    #obj.init_fields()
    exporter.export_objects(objects)
   #exporter.export_pickle(obj)

    # for field in obj.fields:
    #     print("Enter value for field "+field.title)
    #     input_value = input()
    #     obj.set_field_value(field.nam,input_value)

def run_test():
    print("Running Test...")
    create_test_object()