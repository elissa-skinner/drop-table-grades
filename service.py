from models import TableModel

class TableService:
    def __init__(self):
        self.model = TableModel()

    def create(self, params):
        self.model.create(params["text"], params["Description"])