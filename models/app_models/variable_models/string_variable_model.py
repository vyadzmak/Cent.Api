class StringVar():
    def __init__(self,not_null = False,default_value = "",max_length = -1,min_length = -1,input_format ="",output_format =""):
        self.default_value = default_value
        self.max_length = max_length
        self.min_length = min_length
        self.not_null = not_null
        self.input_format =input_format
        self.output_format =output_format


