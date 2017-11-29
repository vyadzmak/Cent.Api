class IntVar():
    def __init__(self,not_null = False,default_value = 0,max_value =-1,min_value =-1):
        self.not_null = not_null
        self.default_value = default_value
        self.max_value =max_value
        self.min_value =min_value
