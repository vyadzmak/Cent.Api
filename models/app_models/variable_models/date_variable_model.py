from datetime import datetime


class DateVar():
    def __init__(self, output_format="", not_null=False):
        self.output_format = output_format
        self.not_null = not_null
