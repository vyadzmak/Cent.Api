from datetime import datetime


class DateVar():
    def __init__(self,not_null=False, output_format=""):
        self.output_format = output_format
        self.not_null = not_null
