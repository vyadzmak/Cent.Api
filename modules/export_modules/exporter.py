import models.app_models.setting_models.setting_model as setting
import modules.json_modules.json_encoder as encoder

import pickle
def export_object(obj):
    export_path =setting.TEMP_FOLDER
    filename = export_path+obj.name+".txt"
    try:
        j = encoder.encode(obj)
        f = open(filename, 'w', encoding='utf-8')
        f.write(j)
        f.close()
    except Exception as e:
        print("Error in exporting: " + str(e))

def export_objects(obj):
    export_path =setting.TEMP_FOLDER
    filename = export_path+"objects.txt"
    try:
        j = encoder.encode(obj)
        f = open(filename, 'w', encoding='utf-8')
        f.write(j)
        f.close()
    except Exception as e:
        print("Error in exporting: " + str(e))
