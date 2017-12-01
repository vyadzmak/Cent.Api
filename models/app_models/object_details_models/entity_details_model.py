class GeneralSection():
    def __init__(self,id):

        pass

class ObjectsSection():
    def __init__(self,id):
        pass

class SubjectsSection():
    def __init__(self,id):
        pass

class DocumentsSection():
    def __init__(self,id):
        pass

class RelationsSections():
    def __init__(self,id):
        pass

class HistorySection():
    def __init__(self,id):
        pass

class ReportsSection():
    def __init__(self,id):
        pass



class EntityDetails():
    def __init__(self, id):
        self.id = id
        self.general_section =GeneralSection(id)
        self.objects_section = ObjectsSection(id)
        self.subjects_section = SubjectsSection(id)
        self.documents_section =DocumentsSection(id)
        self.relations_section = RelationsSections(id)
        self.history_section = HistorySection(id)
        self.reports_section = ReportsSection(id)


        pass

    def init_general_section(self):
        pass

    def init_objects_section(self):
        pass

    def init_subjects_section(self):
        pass

    def init_documents_section(self):
        pass

    def init_relations_section(self):
        pass

    def init_history_section(self):
        pass

    def init_report_section(self):
        pass

    def init_sections(self):
        self.init_general_section()
        self.init_objects_section()
        self.init_subjects_section()
        self.init_documents_section()
        self.init_relations_section()
        self.init_history_section()
        self.init_report_section()

        pass
