import modules.testing_modules.test_module as testing
import models.app_models.dynamic_object_models.dynamic_object_model as dynamic_model
import modules.json_modules.json_encoder as encoder
if __name__ == '__main__':
    try:
        print("Working")
        model = dynamic_model.DynamicObject()
        model.id = '1'
        model.name = 'test'
        s = encoder.encode(model)
        testing.run_test()
    except Exception as e:
        print("Error");