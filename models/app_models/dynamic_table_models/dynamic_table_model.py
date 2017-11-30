class DynamicTableHeader():
    def __init__(self,text,align,value):
        self.text =text
        self.align = align
        self.value = value

        pass

class DynamicTable():
    def __init__(self):
        self.headers =[]
        self.items =[]
        pass

    def init_header_element(self, text,align,value):
        self.headers.append(DynamicTableHeader(text, align, value))

    def init_item(self,item):
        self.items.append(item)