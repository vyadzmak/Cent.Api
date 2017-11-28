import json
import jsonpickle
import pickle
def encode(ob):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        result = jsonpickle.encode(ob, unpicklable=False)
        return result
    except Exception as e:
        print(str(e))
        return ""


