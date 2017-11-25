from datetime import datetime
class DateVar():
    def __init__(self,output_format="",not_null = False,default_value={}):
        self.default_value =default_value
        self.output_format =output_format
        self.not_null = not_null