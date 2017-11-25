import os,sys

#MODULE WITH "CONSTANTS" DO NOT CHANGE ANYTHING
ROOT_DIR =os.path.dirname(os.path.realpath(sys.argv[0]))
    #os.path.dirname(sys.modules['__main__'].__file__)

print("ROOT ="+ROOT_DIR)
#application run mode
DEBUG_MODE = True

#data folder
DATA_FOLDER =ROOT_DIR+"/data/"

#result folder
RESULT_FOLDER =ROOT_DIR+"/results/"

#temp folder
TEMP_FOLDER = ROOT_DIR+"/temp/"

API_URL ="http://127.0.0.1:5000/"

