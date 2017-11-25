import modules.testing_modules.test_module as testing
if __name__ == '__main__':
    try:
        print("Working")
        testing.run_test()
    except Exception as e:
        print("Error");